from django.db import models
from markdownx.models import MarkdownxField
from dostawemo.purchases.models import Purchase


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name = 'Категория')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=50, verbose_name = 'Цвет')

    class Meta:
        verbose_name = 'цвет'
        verbose_name_plural = 'цвета'

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=50, verbose_name = 'Размер')

    class Meta:
        verbose_name = 'размер'
        verbose_name_plural = 'размеры'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name = 'Название')
    description = MarkdownxField(verbose_name = 'Описание')
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='products', verbose_name = 'Закупка')
    price_cost = models.PositiveIntegerField(verbose_name = 'Себестоимость')
    price = models.PositiveIntegerField(verbose_name = 'Цена')
    price_distaweno = models.PositiveIntegerField(verbose_name = 'Цена в Dostawemo')
    price_rrc = models.PositiveIntegerField(verbose_name = 'Рекомендованная розничная цена')
    price_market = models.PositiveIntegerField(verbose_name = 'Цена на Яндекс.Маркете')
    elevated_cashback = models.BooleanField(verbose_name = 'Повышенный кэшбек')
    brand = models.CharField(max_length=255, verbose_name = 'Брэнд')
    categories = models.ManyToManyField(Category, verbose_name = 'Категории')
    colors = models.ManyToManyField(Color, verbose_name = 'Цвета')
    sizes = models.ManyToManyField(Size, verbose_name = 'Размеры')
    video = models.URLField(null=True, blank=True, verbose_name = 'Ссылка на видео')
    featured = models.BooleanField(verbose_name = 'Отображение на главной')
    is_shown = models.BooleanField(verbose_name = 'Отображение пользователям')
    archived = models.BooleanField(verbose_name = 'Поместить в архив')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name = 'Дата и время обновления')
    
    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name = 'Продукт')
    image = models.ImageField(upload_to='images/products/', verbose_name = 'Изображение')

    class Meta:
        verbose_name = 'изображение продукта'
        verbose_name_plural = 'изображения продукта'

    def __str__(self):
        return str(self.id) + " Изображение продукта " + self.product.title