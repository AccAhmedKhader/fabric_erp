import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
def validate_egyptian_phone(value):
 if not re.match(r'^01[0-9]{9}$', value):
 raise ValidationError(_('Enter a valid Egyptian phone number (e.g., 01012345678)'))
def validate_tax_id(value):
 if not re.match(r'^[0-9]{14}$', value):
 raise ValidationError(_('Enter a valid tax ID (14 digits)'))