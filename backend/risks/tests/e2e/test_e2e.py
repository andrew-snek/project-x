from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


def test_e2e(db, field_type_data):
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

    pair = client.post('http://localhost/obtain-token/', {
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
