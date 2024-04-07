import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from utils.models.base import CreateUpdateTimeTrackableModel


class Order(CreateUpdateTimeTrackableModel, models.Model):
    class PaymentType(models.IntegerChoices):
        CARD = 1, _('Карта')
        CASH = 2, _('Наличные')

    class Status(models.IntegerChoices):
        NEW = 1, _('Новый')
        ACCEPTED = 2, _('Принято')
        READY = 3, _('Готово')
        DELIVERY = 4, _('Курьер забрал')
        DELIVERED = 5, _('Доставлено')
        CANCELED = 6, _('Отменен')

    class OrderType(models.IntegerChoices):
        PICKUP = 1, _('Самовывоз')
        DELIVERY = 2, _('Доставка')

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey('commerce.User', verbose_name=_('пользватель'), on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(_('Общая сумма'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    discount_amount = models.DecimalField(_('Скидка'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    final_amount = models.DecimalField(_('Итог'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    status = models.PositiveSmallIntegerField(_('статус'), choices=Status.choices, default=Status.NEW, db_index=True, blank=True)
    discount = models.PositiveSmallIntegerField(
        _('скидка'), validators=[MaxValueValidator(100), MinValueValidator(0)], default=0, null=True, blank=True)
    payment_type = models.PositiveSmallIntegerField(_('способ оплаты'), choices=PaymentType.choices, db_index=True, null=True, blank=True)
    delivered_at = models.DateTimeField(_('доставлено в'), null=True, blank=True)
    is_paid = models.BooleanField(_('Оплачено'), default=False)
    order_type = models.PositiveSmallIntegerField(
        _('Тип заказа'),
        choices=OrderType.choices,
        default=OrderType.PICKUP,
        db_index=True,
    )
    additional_charge = models.DecimalField(
        _('дополнительная плата'), max_digits=10, decimal_places=2, default=0, blank=True)

    company = models.ForeignKey(
        'commerce.Company', related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    number_of_cutlery = models.PositiveIntegerField(_('Приборы'), null=True, blank=True)
    address = models.CharField(_('адрес'), max_length=228, null=True, blank=True)
    comment = models.TextField(_('комментарий'), blank=True, null=True)
    delivery_zone = models.ForeignKey('commerce.CompanyDeliveryZone', on_delete=models.SET_NULL, verbose_name=_('зона доставки'), null=True, blank=True)

    @property
    def delivery_amount(self):
        return self.additional_charge if self.delivery_zone_id else 0
    
    @property
    def paid_amount(self):
        return self.delivery_amount + self.final_amount if self.final_amount else 0
    
    class Meta:
        verbose_name = _(' Заказ')
        verbose_name_plural = _(' Заказы')

    def __str__(self):
        return f"Заказ {self.pk}"
    

class OrderItem(models.Model):
    order = models.ForeignKey('commerce.Order', on_delete=models.CASCADE, related_name='items', verbose_name=_('Заказ'))
    product = models.ForeignKey('commerce.Product', on_delete=models.CASCADE, related_name='orders', verbose_name=_('Продукт'))
    quantity = models.PositiveIntegerField(_('количество'), validators=[MinValueValidator(1)])
    price = models.DecimalField(_('цена'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    total_price = models.DecimalField(_('Общая сумма'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = _('Детали заказа')
        verbose_name_plural = _('Детали заказа')

    def __str__(self):
        return f"{self.product_id} в Заказе {self.order_id}"