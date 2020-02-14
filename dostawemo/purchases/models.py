from django.db import models
from markdownx.models import MarkdownxField
from dostawemo.cities.models import City


class Purchase(models.Model):
    prefix = models.CharField(unique=True, max_length=50, verbose_name = 'Артикул')
    title = models.CharField(max_length=255, verbose_name = 'Название')
    description = MarkdownxField(verbose_name = 'Описание')

    NOT_ACTIVE = 'NA'
    OPENED = 'OP'
    STOPPED = 'ST'
    BILLING = 'BI'
    REOPENED = 'RE'
    MOVING_TO_CITY = 'MO'
    SHIPPING = 'SH'
    PURCHASE_STATUS_CHOICES = [
        (NOT_ACTIVE, 'Не активная'),
        (OPENED, 'Закупка открыта'),
        (STOPPED, 'Уточнение статуса'),
        (BILLING, 'Вытавление счетов'),
        (REOPENED, 'Добор'),
        (MOVING_TO_CITY, 'Доставка в Dostawemo'),
        (SHIPPING, 'Доставка клиентам'),
    ]
    status = models.CharField(
        max_length=2,
        choices=PURCHASE_STATUS_CHOICES,
        default=NOT_ACTIVE,
        verbose_name = 'Статус закупки'
    )

    purchase_count = models.PositiveIntegerField(default=0, verbose_name = 'Сколько раз была собрана закупка')
    producer_city = models.CharField(max_length=255, verbose_name = 'Город поставщик')
    completeness = models.FloatField(default=0, verbose_name = 'Процент завершения')
    required_amount = models.PositiveIntegerField(verbose_name = 'Необходимая сумма')
    collected_amount = models.PositiveIntegerField(default=0, verbose_name = 'Собранная сумма')
    prepayment_amount = models.PositiveIntegerField(default=100, verbose_name = 'Сумма предоплаты')
    start_date = models.DateTimeField(verbose_name = 'Дата и время начала')
    end_date = models.DateTimeField(verbose_name = 'Дата и время окончания')
    image = models.ImageField(upload_to='images/purchases/', verbose_name = 'Изображение')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name = 'Дата и время обновления')

    class Meta:
        verbose_name = 'закупка'
        verbose_name_plural = 'закупки'

    def __str__(self):
        return self.title