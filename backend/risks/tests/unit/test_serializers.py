import pytest
from rest_framework.serializers import ValidationError
from risks.serializers import AbstractRiskSerializer, RiskSerializer


class TestRiskTypeSerializer:
    def test_fail_validation_abstract_fields(self):
        with pytest.raises(ValidationError):
            AbstractRiskSerializer.validate_abstract_fields(None, [])

    def test_success_validation_abstract_fields(self):
        result = AbstractRiskSerializer.validate_abstract_fields(None, 'data')
        assert result == 'data'

    def test_create(self, mocker):
        patched_atomic = mocker.patch(
            'risks.serializers.transaction.atomic'
        )
        patched_AbstractRisk_create = mocker.patch(
            'risks.serializers.AbstractRisk.objects.create'
        )
        patched_AbstractRisk_create.return_value = 'test_abstract_risk'
        patched_AbstractField = mocker.patch(
            'risks.serializers.AbstractField'
        )
        patched_AbstractField.side_effect = lambda **kw: kw

        abstract_risk_data = {
            'abstract_fields': [{'key': 'val'}, {'key2': 'val2'}],
            'some': 'abstract risk data'
        }
        result = AbstractRiskSerializer.create(None, abstract_risk_data)

        assert result == patched_AbstractRisk_create.return_value

        patched_atomic.assert_called_once()
        patched_AbstractField.objects.bulk_create.assert_called_once_with([
            patched_AbstractField(abstract_risk=result, key='val'),
            patched_AbstractField(abstract_risk=result, key2='val2')
        ])
        patched_AbstractRisk_create.assert_called_once_with(
            **abstract_risk_data
        )


@pytest.fixture
def risk_data():
    return {
        'abstract_risk': 1,
        'fields': [
            {'value': 'onlythis'},
            {'value': 'cucumbe'}
        ]
    }


@pytest.fixture
def patched_get_regexes(mocker):
    patched = mocker.patch(
        'risks.serializers.AbstractField.get_regexes'
    )
    patched.return_value = ['^onlythis$', '^.{7}$']
    return patched


@pytest.fixture
def patched_get_non_matching_fields(mocker):
    patched = mocker.patch(
        'risks.serializers.get_non_matching_fields'
    )
    patched.return_value = []
    return patched


class TestRiskSerializer:
    def test_to_representation(self, mocker):
        patched_Field = mocker.patch('risks.serializers.Field')
        patched_FieldSerializer = mocker.patch(
            'risks.serializers.FieldSerializer'
        )
        risk = mocker.MagicMock()
        patched_Field \
            .objects \
            .filter.return_value \
            .order_by.return_value \
            .values.return_value = ['wow', 'test']
        correct_result = {
            'id': risk.id,
            'name': risk.name,
            'abstract_risk': risk.abstract_risk_id,
            'fields': [
                patched_FieldSerializer(field).data for field
                in ['wow', 'test']
            ]
        }

        result = RiskSerializer.to_representation(None, risk)

        assert result == correct_result

    def test_validate(
        self, risk_data,
        patched_get_regexes, patched_get_non_matching_fields
    ):
        result = RiskSerializer.validate(None, risk_data)

        assert result == risk_data
        patched_get_regexes.assert_called_once_with(risk_data['abstract_risk'])
        patched_get_non_matching_fields.assert_called_once_with(
            patched_get_regexes.return_value, risk_data['fields']
        )

    def test_validate_raises_wrong_number_of_fields(
        self, risk_data, patched_get_regexes
    ):
        risk_data['fields'].pop()

        with pytest.raises(ValidationError):
            RiskSerializer.validate(None, risk_data)

    def test_validate_raises_non_matching_fields(
        self, risk_data, patched_get_regexes, patched_get_non_matching_fields
    ):
        patched_get_non_matching_fields.return_value = [0]

        with pytest.raises(ValidationError):
            RiskSerializer.validate(None, risk_data)

    def test_create(self, mocker):
        patched_atomic = mocker.patch(
            'risks.serializers.transaction.atomic'
        )
        patched_Risk_create = mocker.patch(
            'risks.serializers.Risk.objects.create'
        )
        patched_Risk_create.return_value = 'test_risk'
        patched_Field = mocker.patch(
            'risks.serializers.Field'
        )
        patched_Field.side_effect = lambda **kw: kw

        risk_data = {
            'fields': [{'key': 'val'}, {'key2': 'val2'}],
            'some': 'risk data'
        }
        result = RiskSerializer.create(None, risk_data)

        assert result == patched_Risk_create.return_value

        patched_atomic.assert_called_once()
        patched_Field.objects.bulk_create.assert_called_once_with([
            patched_Field(risk=result, key='val'),
            patched_Field(risk=result, key2='val2')
        ])
        patched_Risk_create.assert_called_once_with(
            **risk_data
        )
