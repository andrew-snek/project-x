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


@pytest.fixture
def abstract_risk_data():
    return [
        {
            'name': 'some_abstractrisk_name',
            'abstract_fields': [
                {'field_type': 1, 'label': 'Some label'}
            ]
        },
        {
            'name': 'another_abstractrisk_name',
            'abstract_fields': [
                {'field_type': 2, 'label': 'Label one'},
                {'field_type': 1, 'label': 'Label two'}
            ]
        },
        {
            'name': 'third_abstractrisk_name',
            'abstract_fields': [
                {'field_type': 2, 'label': 'Label one'},
                {'field_type': 1, 'label': 'Label two'}
            ]
        }
    ]

@pytest.fixture
def risk_data():
    return [
        {
            'name': 'risk_name',
            'abstract_risk': 1,
            'fields': [
                { 'value': 'abc' },
            ]
        },
        {
            'name': 'risk_name2',
            'abstract_risk': 2,
            'fields': [
                {'value': 'onlythis'},
                {'value': 'abc'}
            ]
        },
        {
            'name': 'risk_name3',
            'abstract_risk': 2,
            'fields': [
                {'value': 'onlythis'},
                {'value': 'abc'}
            ]
        }
    ]