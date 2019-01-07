import pytest


@pytest.fixture
def field_type_data():
    return [
        {
            'name': 'some_fieldtype_name',
            'widget_type': 0,
            'regex': 'abc'
        },
        {
            'name': 'another_fieldtype_name',
            'widget_type': 1,
            'regex': '^onlythis$'
        },
        {
            'name': 'third_fieldtype_name',
            'widget_type': 3,
            'regex': '^.{7}$'
        }
    ]
