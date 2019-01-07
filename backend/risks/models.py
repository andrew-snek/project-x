from django.db import models


class FieldType(models.Model):
    WIDGET_TYPES = enumerate([
        'OneLineText',
        'MultiLineText',
        'Date',
        'Enum',
    ])
    name = models.CharField(max_length=30, unique=True)
    widget_type = models.PositiveSmallIntegerField(choices=WIDGET_TYPES)
    regex = models.CharField(max_length=3000)
