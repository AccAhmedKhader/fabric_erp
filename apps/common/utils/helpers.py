import uuid
import re
from datetime import datetime
from django.utils import timezone
def generate_uuid(): return uuid.uuid4()
def get_current_egypt_time(): return timezone.localtime(timezone.now())
def format_egyptian_phone(phone):
 if phone.startswith('+'): return phone
 if phone.startswith('0'): return f"+2{phone}"
 if phone.startswith('01'): return f"+2{phone}"
 return phone
def is_valid_uuid(value):
 try: uuid.UUID(str(value)); return True
 except ValueError: return False
class DateRange:
 def __init__(self, start_date, end_date):
 self.start_date = start_date
 self.end_date = end_date
 def __contains__(self, date):
 return self.start_date <= date <= self.end_date
 def days(self):
 return (self.end_date - self.start_date).days