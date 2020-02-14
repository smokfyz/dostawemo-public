# Generated by Django 3.0.2 on 2020-02-03 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200203_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PP', 'Ожидается предоплата'), ('PM', 'Внесена предоплата'), ('PR', 'Возврат предоплаты'), ('FE', 'Ожидается внесение доплаты'), ('FP', 'Доплата внесена'), ('FX', 'Срок внесения предоплаты истек'), ('DE', 'Доставляется до офиса'), ('CL', 'Заказ закрыт')], default='PP', max_length=2, verbose_name='Статус заказа'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('PR', 'Предоплата'), ('SU', 'Доплата')], default='PR', max_length=2, verbose_name='Тип транзакции')),
                ('sberbank_id', models.CharField(max_length=255, verbose_name='ID сбербанка')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order', verbose_name='Заказ')),
            ],
        ),
    ]
