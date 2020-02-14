from .serializers import QuestionSerializer, CreateQuestionSerializer
from .models import Question
from rest_framework import viewsets, generics, permissions, serializers
from django_filters.rest_framework import DjangoFilterBackend


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(moderation=True).order_by('-created_at')
    filterset_fields = ('product',)

    def get_serializer_class(self):
        if self.action == 'list':
            return QuestionSerializer
        if self.action == 'create':
            return CreateQuestionSerializer
        return QuestionSerializer

