import pytest
from django.db.models.deletion import ProtectedError
from rest_framework import generics
from risks.serializers import FieldTypeSerializer
from risks.views import FieldTypeList
from risks.exceptions import CannotDeleteAlreadyInUse


class TestFieldTypeList:
    def test_subclass(self):
        assert issubclass(FieldTypeList, generics.ListCreateAPIView)
        assert issubclass(FieldTypeList, generics.DestroyAPIView)

    def test_serializer_class(self):
        assert FieldTypeList.serializer_class == FieldTypeSerializer

    def test_queryset(self, mocker):
        p_all = mocker.patch('risks.views.FieldType.objects.all')
        p_all.return_value = 'test'

        assert list(FieldTypeList().get_queryset()) == list(p_all())

    def test_perform_destroy_success(self, mocker):
        p_super = mocker.patch('risks.views.super')

        FieldTypeList.perform_destroy(None, 'instance to destroy')

        p_super \
            .return_value \
            .perform_destroy \
            .assert_called_once_with('instance to destroy')

    def test_perform_destroy_failure(self, mocker):
        p_super = mocker.patch('risks.views.super')
        protected_error = ProtectedError('some msg', 'some objs')
        p_super.return_value.perform_destroy.side_effect = protected_error

        with pytest.raises(CannotDeleteAlreadyInUse):
            FieldTypeList.perform_destroy(None, 'instance to destroy')
