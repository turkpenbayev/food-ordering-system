import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from utils.views.validators import PhoneNumberValidator
from utils.models.base import CreateUpdateTimeTrackableModel


class Customer(CreateUpdateTimeTrackableModel, models.Model):

    class Type(models.IntegerChoices):
        BUSSINESS = 1, _('B2B')
        PERSONAL = 2, _('клиент')

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    user = models.OneToOneField('commerce.User', on_delete=models.SET_NULL, verbose_name=_('пользователь'), related_name='customer', null=True, blank=True)
    name = models.CharField(_('название'), max_length=128, null=True, blank=True)
    address = models.CharField(_('адрес'), max_length=228, blank=True)
    customer_type = models.PositiveSmallIntegerField(
        _('Тип клиента'), choices=Type.choices, default=Type.BUSSINESS, db_index=True)
    phone = models.CharField(
        _('Телефон клиента'),
        max_length=12,
        validators=[PhoneNumberValidator()],
    )
    discount = models.PositiveSmallIntegerField(
        _('скидка'), validators=[MaxValueValidator(100), MinValueValidator(0)], default=0)
    
    class Meta:
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')
    
    def __str__(self):
        return f'{self.name} {self.phone}'
