from rest_framework import serializers
from .models import Question


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class CreateQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['product', 'question']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        question = validated_data['question']

        return Question.objects.create(
            user=user,
            product=product,
            question=question
        )