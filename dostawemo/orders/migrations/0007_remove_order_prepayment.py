# Generated by Django 3.0.2 on 2020-02-03 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20200203_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='prepayment',
        ),
    ]
