from django.db import transaction
from rest_framework import serializers
from risks.models import FieldType, AbstractField, AbstractRisk, Field, Risk
from risks.validation_helpers import get_non_matching_fields


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


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('value',)


class RiskSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)

    class Meta:
        model = Risk
        fields = ('id', 'name', 'abstract_risk', 'fields')

    def to_representation(self, risk):
        return {
            'id': risk.id,
            'name': risk.name,
            'abstract_risk': risk.abstract_risk_id,
            'fields': [
                FieldSerializer(field).data for field
                in Field.objects
                        .filter(risk=risk)
                        .order_by('id')
                        .values(*FieldSerializer.Meta.fields)
            ]
        }

    def validate(self, data):
        regexes = AbstractField.get_regexes(data['abstract_risk'])

        if not len(regexes) == len(data['fields']):
            raise serializers.ValidationError('Wrong number of fields')

        non_matching_fields = get_non_matching_fields(regexes, data['fields'])
        if non_matching_fields:
            err_msg = 'Field\'s value doesn\'t match the regex'
            raise serializers.ValidationError({
                'fields': {
                    field_num: {'value': [err_msg]}
                    for field_num in non_matching_fields
                }
            })

        return data

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        with transaction.atomic():
            risk = Risk.objects.create(**validated_data)
            Field.objects.bulk_create([
                Field(risk=risk, **field_data) for field_data in fields_data
            ])
        return risk
