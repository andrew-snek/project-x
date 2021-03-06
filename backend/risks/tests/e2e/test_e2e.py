from unittest.mock import patch  # mocker.patch can't be a context manager
from django.contrib.auth import get_user_model
from django.db import DatabaseError
from rest_framework.test import APIClient


def test_e2e(transactional_db, field_type_data, abstract_risk_data, risk_data):
    client = APIClient()

    # Helpers for testing
    def get(url, correct_result):
        response = client.get(url)
        assert response.status_code == 200
        assert response.data == correct_result

    def post(url, payload, status=201, err=None):
        response = client.post(url, payload, format='json')

        assert response.status_code == status
        if err:  # Either we got errors in expected fields...
            assert [k for k in response.data.keys()] == err
        else:  # or we succesfully created a new thing
            payload['id'] = response.data['id']
            assert response.data == payload

        return response

    def delete(url, status=204, err=None):
        response = client.delete(url)

        assert response.status_code == status
        if err:
            assert [k for k in response.data.keys()] == err

    # Login
    admin = get_user_model().objects.create(
        username='admin', is_staff=True, is_superuser=True
    )
    admin.set_password('admin')
    admin.save()

    pair = client.post('http://localhost/api/v1/obtain-token/', {
        'username': 'admin',
        'password': 'admin'
    }).data
    client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(pair['access']))

    # Test FieldType
    fieldtypes_url = 'http://localhost/api/v1/fieldtypes/'
    url = fieldtypes_url
    get(url, [])  # No FieldTypes at first

    # Create first FieldType
    post(url, field_type_data[0])
    get(url, [field_type_data[0]])

    # Create second FieldType
    post(url, field_type_data[1])
    get(url, [field_type_data[0], field_type_data[1]])

    # An error, if posting nonsense
    post(url, 'nonsense', status=400, err=['non_field_errors'])
    get(url, [field_type_data[0], field_type_data[1]])

    # An error, if posting a FieldType with existing name
    post(url, field_type_data[1], status=400, err=['name'])
    get(url, [field_type_data[0], field_type_data[1]])

    # An error, if one field is empty
    for field in field_type_data[2].keys():
        post(url, {**field_type_data[2], field: ''}, status=400, err=[field])
        get(url, [field_type_data[0], field_type_data[1]])

    # An error, if widget_type is wrong
    field_type_data[2]['widget_type'] = 'WRONG OPTION'
    post(url, field_type_data[2], status=400, err=['widget_type'])

    # Test AbstractRisk
    abstractrisks_url = 'http://localhost/api/v1/abstractrisks/'
    url = abstractrisks_url
    get(url, [])  # No AbstractRisks at first

    # Create first AbstractRisk
    post(url, abstract_risk_data[0])
    get(url, [abstract_risk_data[0]])

    # Create second AbstractRisk. This one with two abstract fields.
    post(url, abstract_risk_data[1])
    get(url, [abstract_risk_data[0], abstract_risk_data[1]])

    # An error, if posting nonsense
    post(url, 'nonsense', status=400, err=['non_field_errors'])

    # An error if posting an AbstractRisk with already existing name
    post(url, abstract_risk_data[1], status=400, err=['name'])
    get(url, [abstract_risk_data[0], abstract_risk_data[1]])

    # An error if trying to post an empty field
    for field in abstract_risk_data[2].keys():
        post(
            url,
            {**abstract_risk_data[2], field: ''},
            status=400,
            err=[field]
        )
        get(url, [abstract_risk_data[0], abstract_risk_data[1]])

    # No changes if error during transaction
    with patch(
        'risks.serializers.AbstractField.objects.bulk_create'
    ) as patched_bulk_create:
        patched_bulk_create.side_effect = DatabaseError('test db error')
        try:
            post(url, abstract_risk_data[2])
        except DatabaseError as e:
            assert 'test db error' in e.args
    get(url, [abstract_risk_data[0], abstract_risk_data[1]])

    # An error if posting an AbstractRisk with wrong FieldType id's
    abstract_risk_data[2]['abstract_fields'][0]['field_type'] = 'WRONG'
    post(url, abstract_risk_data[2], status=400, err=['abstract_fields'])

    # Test Risk
    risks_url = 'http://localhost/api/v1/risks/'
    url = risks_url
    get(url, [])  # No Risks at first

    # Create first Risk
    post(url, risk_data[0])
    get(url, [risk_data[0]])

    # Create a second Risk, of a different AbstractRisk, with 2 Fields
    post(url, risk_data[1])
    get(url, [risk_data[0], risk_data[1]])

    # An error, if posting nonsense
    post(url, 'nonsense', status=400, err=['non_field_errors'])

    # An error, if posting a Risk with existing name
    post(url, risk_data[1], status=400, err=['name'])
    get(url, [risk_data[0], risk_data[1]])

    # An error, if posting an empty field
    for field in risk_data[2].keys():
        post(url, {**risk_data[2], field: ''}, status=400, err=[field])
        get(url, [risk_data[0], risk_data[1]])

    # No changes if error during transaction
    with patch(
        'risks.serializers.Field.objects.bulk_create'
    ) as patched_bulk_create:
        patched_bulk_create.side_effect = DatabaseError('test db error')
        try:
            post(url, risk_data[2])
        except DatabaseError as e:
            assert 'test db error' in e.args
    get(url, [risk_data[0], risk_data[1]])

    # An error, if Fields' values are not matched by FieldTypes' regexes
    risk_data[2]['fields'][0]['value'] = 'NOTJUSTTHIS'
    risk_data[2]['fields'][1]['value'] = 'XYZ'
    resp = post(url, risk_data[2], status=400, err=['fields'])
    assert [k for k in resp.data['fields'].keys()] == [0, 1]
    get(url, [risk_data[0], risk_data[1]])

    # Can't delete AbstractRisk if in use
    res = client.delete(abstractrisks_url+'1')
    assert res.status_code == 409
    assert res.data['detail'].code == 'cannot_delete_already_in_use'
    get(abstractrisks_url, [abstract_risk_data[0], abstract_risk_data[1]])

    # Can delete Risk
    res = client.delete(risks_url+'1')
    assert res.status_code == 204
    get(risks_url, [risk_data[1]])

    # Can't delete FieldType if in use
    res = client.delete(fieldtypes_url+'1')
    assert res.status_code == 409
    assert res.data['detail'].code == 'cannot_delete_already_in_use'
    get(fieldtypes_url, [field_type_data[0], field_type_data[1]])

    # Can delete AbstractRisk, which is now not in use
    res = client.delete(abstractrisks_url+'1')
    assert res.status_code == 204
    get(abstractrisks_url, [abstract_risk_data[1]])
