from .serializers import FeedbackSerializer, CreateFeedbackSerializer
from .models import Feedback
from rest_framework import viewsets, generics, permissions, serializers
from django_filters.rest_framework import DjangoFilterBackend


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.filter(moderation=True).order_by('-created_at')
    filterset_fields = ('product',)

    def get_serializer_class(self):
        if self.action == 'list':
            return FeedbackSerializer
        if self.action == 'create':
            return CreateFeedbackSerializer
        return FeedbackSerializer

