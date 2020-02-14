import json
import urllib
import uuid
import requests
from types import SimpleNamespace
from rest_framework import serializers, status
from .models import Order, Transaction
from dostawemo.purchases.models import Purchase
from dostawemo.purchases.serializers import PurchaseSerializer
from dostawemo.carts.models import Cart, CartItem
from dostawemo.carts.serializers import CartCreateSerializer, CartSerializer
import json
import math


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    cart = CartSerializer(read_only=True)
    purchase = PurchaseSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['url', 'id', 'status', 'total_cost', 'created_at', 'updated_at', 'user', 'purchase', 'cart']


class PaymentSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    def generate_order_bundle(self, cart_items, coefficient):
        items = []

        final_amount = 0
        for id, cart_item in enumerate(cart_items):
            item_amount = math.floor(cart_item.product.price * cart_item.amount * coefficient * 100)
            items.append({
                "positionId": id,
                "name": cart_item.product.title,
                "quantity": {"value": cart_item.amount, "measure": "штук"},
                "itemAmount": item_amount,
                "itemCode": cart_item.product.id,
            })
            final_amount = final_amount + item_amount
        return {'final_amount': math.floor(final_amount), 'order_bundle': '{"cartItems": { "items": %s }}' %json.dumps(items)}

    def generate_payment_url(self, amount, prepayment_amount, language, order_number, username, password, page_view, return_url, fail_url, cart_items):
        res = 'https://3dsec.sberbank.ru/payment/rest/register.do?'

        coefficient = (amount - prepayment_amount) / amount
        order_info = self.generate_order_bundle(cart_items, coefficient)
        res += 'amount=%s' %str(order_info['final_amount']) + \
            '&language=%s' %str(language) + \
            '&orderNumber=%s' %str(order_number) + \
            '&userName=%s' %str(username) + \
            '&password=%s' %str(password) + \
            '&pageView=%s' %str(page_view) + \
            '&returnUrl=%s' %str(return_url) + \
            '&failUrl=%s' %str(fail_url) + \
            '&orderBundle=%s' %str(order_info['order_bundle'])
        return urllib.parse.quote(res, safe='~@#$&()*!+=:;,.?/\'')

    def create(self, validated_data):
        user = self.context['request'].user
        order = validated_data['order']

        if order.status != Order.FULL_PAYMENT_EXPECTED and order.status != Order.PREPAYMENT_MADE:
            return json.dumps({'detail': 'Невозможно сделать доплату с текущим статусом заказа'})

        request_url = self.generate_payment_url(
            order.total_cost * 100,
            order.purchase.prepayment_amount * 100,
            'ru',
            str(uuid.uuid4()).replace('-', ''),
            'dostawemo-api',
            "dostawemo",
            "DESKTOP",
            "https://ivansharapenkov.pythonanywhere.com/api/orders/success-payment",
            "https://ivansharapenkov.pythonanywhere.com/api/orders/fail-payment",
            CartItem.objects.filter(cart=order.cart)
        )

        response = requests.get(request_url)

        print(json.loads(response.content))

        Transaction.objects.create(
            order=order,
            sberbank_id=json.loads(response.content)["orderId"],
            type=Transaction.SURCHARGE
        )

        return response.content


class PrepaymentSerializer(serializers.Serializer):
    purchase = serializers.PrimaryKeyRelatedField(queryset=Purchase.objects.all())
    cart_items = CartCreateSerializer(many=True)
    delivery_type = serializers.CharField(max_length=255)
    delivery_address = serializers.CharField(max_length=500)

    def generate_order_bundle(self, cart_items):
        items = []

        for id, cart_item in enumerate(cart_items):
            items.append({
                "positionId": id,
                "name": cart_item.title,
                "quantity": {"value": cart_item.amount, "measure": "штук"},
                "itemAmount": cart_item.price * cart_item.amount * 100,
                "itemCode": cart_item.id,
            })
        return '{"cartItems": { "items": %s }}' %json.dumps(items)

    def generate_payment_url(self, amount, language, order_number, username, password, page_view, return_url, fail_url, cart_items):
        res = 'https://3dsec.sberbank.ru/payment/rest/register.do?'
        order_bundle = self.generate_order_bundle(cart_items)

        res += 'amount=%s' %str(amount) + \
            '&language=%s' %str(language) + \
            '&orderNumber=%s' %str(order_number) + \
            '&userName=%s' %str(username) + \
            '&password=%s' %str(password) + \
            '&pageView=%s' %str(page_view) + \
            '&returnUrl=%s' %str(return_url) + \
            '&failUrl=%s' %str(fail_url) + \
            '&orderBundle=%s' %str(order_bundle)
        return urllib.parse.quote(res, safe='~@#$&()*!+=:;,.?/\'');

    def create(self, validated_data):
        user = self.context['request'].user
        purchase = validated_data['purchase']
        cart_items = validated_data['cart_items']
        delivery_type = validated_data['delivery_type']
        delivery_address = validated_data['delivery_address']

        if not all(item['product'].purchase == purchase for item in cart_items):
            return {"status": status.HTTP_400_BAD_REQUEST, "message": json.dumps({'detail': 'Продукты принадлежат разным закупкам'})}

        order = None
        for cart_item in cart_items:
            try:
                cart = Cart.objects.get(user=user, purchase=purchase)
                order = Order.objects.get(cart=cart)
                print(order.status, Order.PREPAYMENT)
                if order.status != Order.PREPAYMENT and order.status != Order.PREPAYMENT_MADE:
                    raise Cart.DoesNotExist
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=user, purchase=purchase)

            try:
                item = CartItem.objects.get(cart=cart, color=cart_item['color'], size=cart_item['size'], product=cart_item['product'])
                item.amount = item.amount + cart_item['amount']
                item.save()
            except CartItem.DoesNotExist:
                item = CartItem.objects.create(cart=cart, **cart_item)

        total_cost = sum([item.product.price*item.amount for item in CartItem.objects.filter(cart=cart)])

        if order:
            order.total_cost = total_cost
            order.save()
            purchase = order.purchase
            purchase.collected_amount = purchase.collected_amount + order.total_cost
            purchase.completeness = purchase.collected_amount / purchase.required_amount
            purchase.save()
            return {"status": status.HTTP_200_OK, "message": json.dumps(OrderSerializer(order, context=self.context).data)}
        else:
            order = Order.objects.create(
                user=user,
                purchase=purchase,
                cart=cart,
                total_cost=total_cost
            )

        prepayment = [{
            'id': 3,
            'title': 'Предоплата к заказу %s' %(order.id),
            'price': cart.purchase.prepayment_amount,
            'amount': 1
        }]

        prepayment = [SimpleNamespace(**prepayment[0])]

        request_url = self.generate_payment_url(
            cart.purchase.prepayment_amount * 100,
            'ru',
            str(uuid.uuid4()).replace('-', ''),
            'dostawemo-api',
            "dostawemo",
            "DESKTOP",
            "https://ivansharapenkov.pythonanywhere.com/api/orders/success-prepayment",
            "https://ivansharapenkov.pythonanywhere.com/api/orders/fail-prepayment",
            prepayment
        )

        response = requests.get(request_url)

        Transaction.objects.create(
            order=order,
            sberbank_id=json.loads(response.content)["orderId"]
        )

        return {"status": status.HTTP_201_CREATED, "message": response.content}