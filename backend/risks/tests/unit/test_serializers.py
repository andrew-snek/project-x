import pytest
from rest_framework.serializers import ValidationError
from risks.serializers import AbstractRiskSerializer


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
