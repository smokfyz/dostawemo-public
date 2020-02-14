from rest_framework import serializers
from .models import CartItem, Cart
from dostawemo.products.serializers import ColorSerializer, SizeSerializer, ProductSerializer
from dostawemo.products.models import Product, Size, Color
from dostawemo.purchases.models import Purchase


class CartItemSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'url',
            'product',
            'color',
            'size',
            'amount',
        ]


class CartSerializer(serializers.HyperlinkedModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'url',
            'purchase',
            'items',
        ]


class CartCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all())
    size = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all())
    amount = serializers.IntegerField(max_value=32767, min_value=1)

    def create(self, validated_data):
        user = self.context['request'].user
        purchase = validated_data['product'].purchase

        try:
            cart = Cart.objects.get(user=user, purchase=purchase)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user, purchase=purchase)

        try:
            item = CartItem.objects.get(cart=cart, color=validated_data['color'], size=validated_data['size'], product=validated_data['product'])
            item.amount = item.amount + validated_data['amount']
            item.save()
        except CartItem.DoesNotExist:
            item = CartItem.objects.create(cart=cart, **validated_data)

        return item