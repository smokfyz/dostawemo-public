# Generated by Django 3.0.2 on 2020-01-22 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('purchases', '0003_auto_20200120_1142'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0002_auto_20200121_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PM', 'Внесена предоплата'), ('PR', 'Возврат предоплаты'), ('FE', 'Ожидается внесение доплаты'), ('FP', 'Доплата внесена'), ('FX', 'Срок внесения предоплаты истек'), ('DE', 'Доставляется до офиса'), ('CL', 'Заказ закрыт')], default='PM', max_length=2, verbose_name='Статус заказа')),
                ('prepayment', models.BooleanField(verbose_name='Предоплата внесена')),
                ('prepayment_amount', models.PositiveIntegerField(verbose_name='Размер предоплаты')),
                ('total_cost', models.PositiveIntegerField(verbose_name='Итоговая сумма заказа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.Purchase', verbose_name='Закупка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
            },
        ),
    ]
