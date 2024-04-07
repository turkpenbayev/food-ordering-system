from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import _get_error_details, APIException


class ActionError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'action_error'
    default_detail = _('Can not perform action.')

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _get_error_details(detail, code)
        self.code = code
