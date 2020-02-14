from django.db import models
from dostawemo.products.models import Product
from django.contrib.auth import get_user_model


User = get_user_model()


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = 'Продукт')
    question = models.TextField(verbose_name = 'Вопрос')
    answer = models.TextField(verbose_name = 'Ответ')
    moderation = models.BooleanField(default=False, verbose_name = 'Модерация пройдена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name = 'Дата и время обновления')
    
    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return str(self.question)
