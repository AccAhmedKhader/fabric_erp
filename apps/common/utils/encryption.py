import hashlib
import hmac
import base64
from cryptography.fernet import Fernet
from django.conf import settings
import logging
logger = logging.getLogger(__name__)
class EncryptionUtils:
 def __init__(self):
 key = settings.SECRET_KEY[:32].encode()
 self.cipher = Fernet(base64.urlsafe_b64encode(key))
 def encrypt(self, text):
 try:
 return self.cipher.encrypt(text.encode()).decode()
 except Exception as e:
 logger.error(f"Encryption error: {str(e)}\")
 return None
 def decrypt(self, encrypted_text):
 try:
 return self.cipher.decrypt(encrypted_text.encode()).decode()
 except Exception as e:
 logger.error(f"Decryption error: {str(e)}\")
 return None
 @staticmethod
 def hash_value(value):
 return hashlib.sha256(value.encode()).hexdigest()
 @staticmethod
 def verify_hmac(value, signature, secret):
 expected = hmac.new(secret.encode(), value.encode(), hashlib.sha256).hexdigest()
 return hmac.compare_digest(expected, signature)