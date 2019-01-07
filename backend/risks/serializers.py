from rest_framework import serializers
from risks.models import FieldType


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ('id', 'name', 'widget_type', 'regex')
