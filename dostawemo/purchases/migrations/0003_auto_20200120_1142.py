# Generated by Django 3.0.2 on 2020-01-20 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0002_auto_20200120_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='collected_amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Собранная сумма'),
        ),
    ]