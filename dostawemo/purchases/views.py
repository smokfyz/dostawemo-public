from .models import Purchase
from django.db.models import F
from rest_framework import viewsets, generics, permissions, serializers, filters
from .serializers import PurchaseSerializer


class PurchaseFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.annotate(completion=(F('collected_amount')/F('required_amount'))).order_by('completion')


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all().order_by('-created_at')
    serializer_class = PurchaseSerializer
    filter_backends = [filters.OrderingFilter,]
    ordering_fields = ['created_at','completeness',]

