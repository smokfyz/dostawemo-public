from django.db import models
from dostawemo.users.models import User
from dostawemo.products.models import Product, Color, Size
from dostawemo.purchases.models import Purchase


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Пользователь')
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name = 'Закупка')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = 'Товар')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name = 'Цвет')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name = 'Размер')
    amount = models.PositiveIntegerField(default=1, verbose_name = 'Количество')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name = 'Корзина')

    class Meta:
        verbose_name = 'элемент корзины'
        verbose_name_plural = 'элементы корзины'

    def __str__(self):
        return str(self.id)