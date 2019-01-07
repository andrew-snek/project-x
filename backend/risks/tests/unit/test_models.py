from risks.models import FieldType, AbstractField, AbstractRisk


class TestFieldType:
    def test_fields(self):
        for field in ['name', 'widget_type', 'regex']:
            getattr(FieldType, field)


class TestAbstractField:
    def test_fields(self):
        for field in ['field_type', 'abstract_risk', 'label']:
            getattr(AbstractField, field)

    def test_get_regexes(self, mocker):
        patched_objects = mocker.patch(
            'risks.models.AbstractField.objects'
        )
        patched_objects \
            .filter.return_value \
            .order_by.return_value \
            .values_list.return_value = 'correct regexes'

        result = AbstractField.get_regexes('some abstract risk')

        patched_objects.filter.assert_called_once_with(
            abstract_risk='some abstract risk'
        )
        patched_objects \
            .filter.return_value \
            .order_by.assert_called_once_with('id')
        patched_objects \
            .filter.return_value \
            .order_by.return_value \
            .values_list.assert_called_once_with(
                'field_type__regex', flat=True
            )
        assert result == 'correct regexes'


class TestAbstractRisk:
    def test_fields(self):
        for field in ['name', 'field_types']:
            getattr(AbstractRisk, field)
