# Generated by Django 3.0.2 on 2020-01-09 00:31

from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('purchases', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Цвет')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', markdownx.models.MarkdownxField(verbose_name='Описание')),
                ('price_cost', models.PositiveIntegerField(verbose_name='Себестоимость')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('price_distaweno', models.PositiveIntegerField(verbose_name='Цена в Dostawemo')),
                ('price_rrc', models.PositiveIntegerField(verbose_name='Рекомендованная розничная цена')),
                ('price_market', models.PositiveIntegerField(verbose_name='Цена на Яндекс.Маркете')),
                ('elevated_cashback', models.BooleanField(verbose_name='Повышенный кэшбек')),
                ('brand', models.CharField(max_length=255, verbose_name='Брэнд')),
                ('video', models.URLField(verbose_name='Ссылка на видео')),
                ('featured', models.BooleanField(verbose_name='Отображение на главной')),
                ('is_shown', models.BooleanField(verbose_name='Отображение пользователям')),
                ('archived', models.BooleanField(verbose_name='Заархивировать')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')),
                ('categories', models.ManyToManyField(to='products.Category', verbose_name='Категории')),
                ('colors', models.ManyToManyField(to='products.Color', verbose_name='Цвета')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.Purchase', verbose_name='Закупка')),
            ],
            options={
                'verbose_name': 'закупка',
                'verbose_name_plural': 'закупки',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Размер')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.Product', verbose_name='Продукт')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(to='products.Size', verbose_name='Размеры'),
        ),
    ]
