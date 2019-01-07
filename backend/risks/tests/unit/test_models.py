from risks.models import FieldType


class TestFieldType:
    def test_fields(self):
        for field in ['name', 'widget_type', 'regex']:
            getattr(FieldType, field)
