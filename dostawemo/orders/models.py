from django.db import models
from dostawemo.users.models import User
from dostawemo.purchases.models import Purchase    
from dostawemo.carts.models import Cart 


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Пользователь')
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name = 'Закупка')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name = 'Корзина')

    PREPAYMENT = 'PP'
    PREPAYMENT_MADE = 'PM'
    PREPAYMENT_RETURN = 'PR'
    FULL_PAYMENT_EXPECTED = 'FE'
    FULL_PAYMENT_MADE = 'FP'
    FULL_PAYMENT_EXPIRED = 'FX'
    DELIVERED = 'DE'
    CLOSED = 'CL'
    ORDER_STATUS_CHOICES = [
        (PREPAYMENT, 'Ожидается предоплата'),
        (PREPAYMENT_MADE, 'Внесена предоплата'),
        (PREPAYMENT_RETURN, 'Возврат предоплаты'),
        (FULL_PAYMENT_EXPECTED, 'Ожидается внесение доплаты'),
        (FULL_PAYMENT_MADE, 'Доплата внесена'),
        (FULL_PAYMENT_EXPIRED, 'Срок внесения предоплаты истек'),
        (DELIVERED, 'Доставляется до офиса'),
        (CLOSED, 'Заказ закрыт'),
    ]
    status = models.CharField(
        max_length=2,
        choices=ORDER_STATUS_CHOICES,
        default=PREPAYMENT,
        verbose_name = 'Статус заказа'
    )

    #COURIER = 'CO'
    #MAIL = 'MA'
    #OFFICE = 'OF'
    #PVZ = 'PV'
    #TRANSPORT_COMPANY = 'TC'
    #ORDER_STATUS_CHOICES = [
    #    (COURIER, 'Курьев'),
    #    (MAIL, 'Почта'),
    #    (OFFICE, 'Офис'),
    #    (PVZ, 'Пункт выдачи заказов'),
    #    (TRANSPORT_COMPANY, 'Транспортная компанияЦ'),
    #]
    #delivery_type = models.CharField(
    #    max_length=2,
    #    choices=ORDER_STATUS_CHOICES,
    #    default=PREPAYMENT_MADE,
    #    verbose_name = 'Статус заказа'
    #)
    total_cost = models.PositiveIntegerField(verbose_name = 'Итоговая сумма заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name = 'Дата и время обновления')
    
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return str(self.user)


class Transaction(models.Model):
    PREPAYMENT = 'PR'
    SURCHARGE = 'SU'
    TYPE_CHOICES = [
        (PREPAYMENT, 'Предоплата'),
        (SURCHARGE, 'Доплата'),
    ]
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=PREPAYMENT,
        verbose_name = 'Тип транзакции'
    )
    sberbank_id = models.CharField(max_length=255, verbose_name = 'ID сбербанка')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name = 'Заказ')

    class Meta:
        verbose_name = 'транзакция'
        verbose_name_plural = 'транзакции'

    def __str__(self):
        return self.sberbank_id

