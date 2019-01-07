from rest_framework.exceptions import APIException
from risks.exceptions import CannotDeleteAlreadyInUse


class TestCannotDeleteAlreadyInUse:
    def test_subclass(self):
        assert issubclass(CannotDeleteAlreadyInUse, APIException)

    def test_default_status_code(self):
        assert CannotDeleteAlreadyInUse.status_code == 409

    def test_default_detail(self):
        assert (
            CannotDeleteAlreadyInUse
            .default_detail == 'Cannot delete, already in use.'
        )

    def test_default_code(self):
        assert (
            CannotDeleteAlreadyInUse
            .default_code == 'cannot_delete_already_in_use'
        )
