from rest_framework import serializers
from .models import Product, Category, Color, Size, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = ProductImage
        fields = [ 'url', 'image', ]

    def get_image_url(self, obj):
        return "http://" + self.context['request'].get_host() + "/" + obj.image.url


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    purchase_id = serializers.ReadOnlyField(source='purchase.id')
    purchase_title = serializers.ReadOnlyField(source='purchase.title')
    purchase_prefix = serializers.ReadOnlyField(source='purchase.prefix')


    class Meta:
        model = Product
        fields = '__all__'