# Generated by Django 3.0.2 on 2020-01-09 00:32

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=50, unique=True, verbose_name='Артикул')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', markdownx.models.MarkdownxField(verbose_name='Описание')),
                ('status', models.CharField(choices=[('NA', 'Не активная'), ('OP', 'Закупка открыта'), ('ST', 'Уточнение статуса'), ('BI', 'Вытавление счетов'), ('RE', 'Добор'), ('MO', 'Доставка в Dostawemo'), ('SH', 'Доставка клиентам')], default='NA', max_length=2, verbose_name='Статус закупки')),
                ('producer_city', models.CharField(max_length=255, verbose_name='Город поставщик')),
                ('required_amount', models.PositiveIntegerField(verbose_name='Необходимая сумма')),
                ('collected_amount', models.PositiveIntegerField(verbose_name='Собранная сумма')),
                ('start_date', models.DateTimeField(verbose_name='Дата и время начала')),
                ('end_date', models.DateTimeField(verbose_name='Дата и время окончания')),
                ('image', models.ImageField(upload_to='images/purchases/', verbose_name='Изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')),
            ],
            options={
                'verbose_name': 'закупка',
                'verbose_name_plural': 'закупки',
            },
        ),
    ]
