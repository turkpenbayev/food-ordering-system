from django.db import models
from django.utils.translation import gettext_lazy as _


class FakeDeletableModel(models.Model):
    deleted = models.BooleanField(_('deleted'), default=False, db_index=True)

    class Meta:
        abstract = True

    def fake_delete(self):
        if self.deleted:
            raise ValueError('Already deleted.')
        self.deleted = True
        self.save(update_fields=['deleted'])


class CreateTimeTrackableModel(models.Model):
    created_at = models.DateTimeField(
        _('создан в'), auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class UpdateTimeTrackableModel(models.Model):
    modified_at = models.DateTimeField(_('изменено в'), auto_now=True)

    class Meta:
        abstract = True


class CreateUpdateTimeTrackableModel(CreateTimeTrackableModel, UpdateTimeTrackableModel):
    class Meta:
        abstract = True


class CreatedByTrackableModel(models.Model):
    created_by_id = models.IntegerField(
        verbose_name=_('created_by'), db_index=True)

    class Meta:
        abstract = True
