from rest_framework.exceptions import APIException


class CannotDeleteAlreadyInUse(APIException):
    status_code = 409
    default_detail = 'Cannot delete, already in use.'
    default_code = 'cannot_delete_already_in_use'
