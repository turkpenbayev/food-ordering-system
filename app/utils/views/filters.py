from django.db import models
from django_filters import NumberFilter, FilterSet


class IntegerForeignKeyFilterSet(FilterSet):
    class Meta:
        filter_overrides = {
            models.ForeignKey: {
                'filter_class': NumberFilter,
            }
        }
