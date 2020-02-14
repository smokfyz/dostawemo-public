from rest_framework import serializers
from .models import Purchase
from dostawemo.products.serializers import ProductSerializer


class PurchaseSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = [
            'url',
            'prefix',
            'title',
            'description',
            'status',
            'producer_city',
            'purchase_count',
            'completeness',
            'required_amount',
            'collected_amount',
            'prepayment_amount',
            'start_date',
            'end_date',
            'image',
            'products',
        ]

    def get_image_url(self, obj):
        return "http://" + self.context['request'].get_host() + "/" + obj.image.url