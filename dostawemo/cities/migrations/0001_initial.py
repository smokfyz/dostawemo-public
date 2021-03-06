# Generated by Django 3.0.2 on 2020-01-07 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Название')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities.Country', verbose_name='Страна')),
            ],
        ),
    ]
