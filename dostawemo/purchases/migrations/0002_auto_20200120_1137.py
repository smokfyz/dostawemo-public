# Generated by Django 3.0.2 on 2020-01-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='collected_amount',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Собранная сумма'),
        ),
    ]
