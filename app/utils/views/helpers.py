from django.conf import settings
from django.utils.translation import get_language
from rest_framework.exceptions import ParseError


def int_from_view_kwargs(view, key):
    return to_digit_key(from_view_kwargs(view, key))


def from_view_kwargs(view, key):
    arg = view.kwargs.get(key)
    if key is None:
        raise ParseError
    return arg


def to_digit_key(key: str):
    if key.isdigit():
        return int(key)
    else:
        raise ParseError
