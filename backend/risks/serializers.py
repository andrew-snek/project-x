from django.db import transaction
from rest_framework import serializers
from risks.models import FieldType, AbstractField, AbstractRisk


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ('id', 'name', 'widget_type', 'regex')


class AbstractFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractField
        fields = ('field_type', 'label')


class AbstractRiskSerializer(serializers.ModelSerializer):
    abstract_fields = AbstractFieldSerializer(many=True)

    class Meta:
        model = AbstractRisk
        fields = ('id', 'name', 'abstract_fields')

    def validate_abstract_fields(self, data):
        if not data:
            raise serializers.ValidationError
        return data

    def create(self, validated_data):
        abstract_fields_data = validated_data.pop('abstract_fields')
        with transaction.atomic():
            abstract_risk = AbstractRisk.objects.create(**validated_data)
            AbstractField.objects.bulk_create([
                AbstractField(
                    abstract_risk=abstract_risk,
                    **abstract_field_data
                ) for abstract_field_data in abstract_fields_data
            ])
            return abstract_risk
