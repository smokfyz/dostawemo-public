# Generated by Django 3.0.2 on 2020-01-07 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'город', 'verbose_name_plural': 'города'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'страна', 'verbose_name_plural': 'страны'},
        ),
    ]