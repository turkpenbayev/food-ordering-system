import os
import uuid

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from utils.views.validators import FileValidator

from utils.models.base import CreateUpdateTimeTrackableModel


def get_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    return os.path.join('products', f'{uuid.uuid4()}{ext}')


class Product(CreateUpdateTimeTrackableModel, models.Model):
    validate_image = FileValidator(max_size=1024 * 1024 * 1, content_types=('image/jpeg', 'image/png'))

    category = models.ForeignKey('commerce.Category', on_delete=models.SET_NULL, verbose_name=_('категория'), null=True, blank=True)
    name = models.CharField(_('название'), max_length=128)
    description = models.CharField(_('описание'), max_length=300, blank=True)
    image = models.ImageField(_('изображение'), validators=[validate_image], upload_to=get_upload_path, blank=True)
    cost_price = models.DecimalField(_('себестоимость'), max_digits=10, decimal_places=2)
    price = models.DecimalField(_('цена'), max_digits=10, decimal_places=2)
    order = models.PositiveIntegerField(_('порядок'), default=9999)
    hide = models.BooleanField(_('скрыт'), default=False)

    class Meta:
        verbose_name = _(' Продукт')
        verbose_name_plural = _(' Продукты')
        unique_together = ('category_id', 'name')

    def __str__(self):
        return f'{self.name} {self.price}'
