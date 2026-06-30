"""
Shared validation utilities.
"""

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_egyptian_id(value):
    """
    Validate Egyptian national ID (14 digits).
    """
    if not re.match(r'^[0-9]{14}$', value):
        raise ValidationError(_('Enter a valid Egyptian ID (14 digits)'))


def validate_egyptian_phone(value):
    """
    Validate Egyptian phone number.
    """
    if not re.match(r'^01[0-9]{9}$', value):
        raise ValidationError(_('Enter a valid Egyptian phone number (e.g., 01012345678)'))


def validate_currency(value):
    """
    Validate ISO currency code (3 letters).
    """
    if len(value) != 3 or not value.isalpha():
        raise ValidationError(_('Enter a valid ISO currency code (3 letters)'))


def validate_date_format(value):
    """
    Validate date format string.
    """
    formats = ['d/m/Y', 'm/d/Y', 'Y-m-d', 'd-m-Y', 'm-d-Y']
    if value not in formats:
        raise ValidationError(_('Enter a valid date format'))


def validate_tax_id(value):
    """
    Validate tax ID (14 digits).
    """
    if not re.match(r'^[0-9]{14}$', value):
        raise ValidationError(_('Enter a valid tax ID (14 digits)'))