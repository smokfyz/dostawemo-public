from .serializers import OrderSerializer, PrepaymentSerializer, PaymentSerializer
from .models import Order, Transaction
from rest_framework import viewsets, generics, permissions, serializers, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import json


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class PaymentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = self.perform_create(serializer)
        return Response(json.loads(res), status=status.HTTP_201_CREATED)


@api_view(['GET'])
def SuccessPaymentView(request):
    order_id = request.GET["orderId"]
    order = Transaction.objects.get(sberbank_id=order_id, type=Transaction.SURCHARGE).order
    order.status = Order.FULL_PAYMENT_MADE
    order.save()
    return Response({'detail': 'Доплата успещно выполнена'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def FailPaymentView(request):
    order_id = request.GET["orderId"]
    Transaction.objects.get(sberbank_id=order_id, type=Transaction.SURCHARGE).order.delete()
    Transaction.objects.get(sberbank_id=order_id, type=Transaction.SURCHARGE).delete()
    return Response(request.GET, status=status.HTTP_400_BAD_REQUEST)


class PrepaymentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PrepaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = self.perform_create(serializer)
        return Response(json.loads(res["message"]), status=res["status"])


@api_view(['GET'])
def SuccessPrepaymentView(request):
    order_id = request.GET["orderId"]
    order = Transaction.objects.get(sberbank_id=order_id, type=Transaction.PREPAYMENT).order
    order.status = Order.FULL_PAYMENT_EXPECTED
    order.save()
    purchase = order.purchase
    purchase.collected_amount = purchase.collected_amount + order.total_cost
    purchase.completeness = purchase.collected_amount / purchase.required_amount
    purchase.save()
    return Response({'detail': 'Предоплата успещно выполнена'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def FailPrepaymentView(request):
    order_id = request.GET["orderId"]
    Transaction.objects.get(sberbank_id=order_id, type=Transaction.PREPAYMENT).order.delete()
    Transaction.objects.get(sberbank_id=order_id, type=Transaction.PREPAYMENT).delete()
    return Response(request.GET, status=status.HTTP_400_BAD_REQUEST)