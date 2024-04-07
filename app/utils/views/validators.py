import magic
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import RegexValidator
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class FileValidator(object):
    """ File validator

    Ensures size and content type of a file.
    """
    error_messages = {
        "max_size": _("Ensure this file size is not greater than %(max_size)s."
                      " Your file size is %(size)s."),
        "content_type": _("Files of type %(content_type)s are not supported.")
    }

    def __init__(self, max_size=None, content_types=()):
        self.max_size = max_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise DjangoValidationError(self.error_messages['max_size'], 'max_size', params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            if content_type not in self.content_types:
                params = {'content_type': content_type}
                raise DjangoValidationError(self.error_messages['content_type'], 'content_type', params)

    def __eq__(self, other):
        return isinstance(other, FileValidator)


@deconstructible
class PhoneNumberValidator(RegexValidator):
    """ Phone number validator

    Validates phone number via regular expression
    """

    def __init__(self, message=None):
        super(PhoneNumberValidator, self).__init__(
            regex=r'^(\+77)\d{9}$',
            message=message or _("Phone number must be entered in the format: '+77xxyyyzzzz'"),
            code='invalid_phone'
        )
