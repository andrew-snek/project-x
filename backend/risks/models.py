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


class AbstractField(models.Model):
    field_type = models.ForeignKey(FieldType, on_delete=models.PROTECT)
    abstract_risk = models.ForeignKey(
        'AbstractRisk',
        on_delete=models.CASCADE,
        related_name='abstract_fields'
    )
    label = models.CharField(max_length=30)

    @classmethod
    def get_regexes(cls, abstract_risk):
        return cls.objects \
                  .filter(abstract_risk=abstract_risk) \
                  .order_by('id') \
                  .values_list('field_type__regex', flat=True)


class AbstractRisk(models.Model):
    name = models.CharField(max_length=30, unique=True)
    field_types = models.ManyToManyField(
        'FieldType',
        through='AbstractField',
        related_name='abstract_risks'
    )
