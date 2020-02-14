from .serializers import CartSerializer, CartItemSerializer, CartCreateSerializer
from .models import CartItem, Cart
from rest_framework import viewsets, generics, permissions, serializers, status
from rest_framework.response import Response


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CartCreateSerializer
        return CartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'detail': 'Продукт успешно добавлен в корзину'}, status=status.HTTP_201_CREATED, headers=headers)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer