import pytest
from risks.validation_helpers import get_non_matching_fields

@pytest.fixture
def regexes():
    return ['abc', '^onlythis$', '^.{7}$']


field_values = ['abcd', 'onlythis', '123f567']
@pytest.fixture
def fields():
    return [
        {'value': v} for v in field_values
    ]


class TestGetNonMatchingFields:
    def test_all_fields_match(self, regexes, fields):
        nmf = get_non_matching_fields(regexes, fields)

        assert nmf == []

    @pytest.mark.parametrize("wrong_field_index", range(len(field_values)))
    def test_one_field_doesnt_match(
        self, regexes, fields, wrong_field_index
    ):
        fields[wrong_field_index]['value'] = 'INCORRECT VALUE'

        nmf = get_non_matching_fields(regexes, fields)

        assert nmf == [wrong_field_index]

    def test_all_fields_dont_match(self, regexes, fields):
        fields = [{'value': 'INCORRECT VALUE'}] * len(fields)

        nmf = get_non_matching_fields(regexes, fields)

        assert nmf == [0, 1, 2]
