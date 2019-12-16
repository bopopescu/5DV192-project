from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.utils import json


def is_empty_json(json):
    if len(json) > 0:
        return False
    else:
        return True


def is_email_valid(email):
    try:
        validate_email(email)
    except ValidationError:
        return False
    else:
        return True

