from .serializers import ProductSerializer, CategorySerializer, ColorSerializer, SizeSerializer, ProductImageSerializer
from .models import Product, Category, Color, Size, ProductImage
from rest_framework import viewsets, generics, permissions, serializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_shown=True, archived=False).order_by('-created_at')
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer