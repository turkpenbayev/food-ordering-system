import os
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.views.validators import FileValidator, PhoneNumberValidator


def get_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    return os.path.join('companies', f'{uuid.uuid4()}{ext}')


class CompanyDeliveryZone(models.Model):
    company = models.ForeignKey(
        'commerce.Company', related_name='delivery_zones', on_delete=models.CASCADE)
    name = models.CharField(_('название зоны'), max_length=255)
    additional_charge = models.DecimalField(
        _('дополнительная плата'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('зона доставки')
        verbose_name_plural = _('зоны доставки')

    def __str__(self):
        return f'{self.name} {self.additional_charge}'


class Company(models.Model):
    validate_image = FileValidator(
        max_size=1024 * 1024 * 1, content_types=('image/jpeg', 'image/png'))

    logo = models.ImageField(
        _('логотип'), upload_to=get_upload_path, null=True, blank=True)
    name = models.CharField(_('название'), max_length=255)
    instagram = models.URLField(_('Instagram'), null=True, blank=True)
    whatsapp = models.CharField(
        _('WhatsApp'), max_length=20, null=True, blank=True)
    phone_number = models.CharField(
        _('номер телефона'), max_length=12, validators=[PhoneNumberValidator()],)
    address = models.TextField(_('адрес'))

    class Meta:
        verbose_name = _('Компания')
        verbose_name_plural = _('Компании')

    def __str__(self):
        return self.name
