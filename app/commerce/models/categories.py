from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models.base import CreateUpdateTimeTrackableModel


class Category(CreateUpdateTimeTrackableModel, models.Model):
    company = models.ForeignKey(
        'commerce.Company', related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(_('название'), max_length=128, unique=True)
    order = models.PositiveIntegerField(_('порядок'), default=9999)
    hide = models.BooleanField(_('скрыт'), default=False)

    class Meta:
        verbose_name = _(' Категория')
        verbose_name_plural = _(' Категории')

    def __str__(self,):
        return self.name
