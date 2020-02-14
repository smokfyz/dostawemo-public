from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class CreateFeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feedback
        fields = ['product', 'video']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        video = validated_data['video']

        return Feedback.objects.create(
            user=user,
            product=product,
            video=video
        )