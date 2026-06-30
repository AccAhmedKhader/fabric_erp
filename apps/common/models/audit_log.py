import uuid
from django.db import models
from django.conf import settings
class AuditLog(models.Model):
 class Meta:
 db_table = 'common_audit_logs'
 verbose_name = 'Audit Log'
 verbose_name_plural = 'Audit Logs'
 ordering = ['-created_at']
 id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
 user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
 action = models.CharField(max_length=100)
 module = models.CharField(max_length=50)
 object_id = models.UUIDField(null=True, blank=True)
 object_type = models.CharField(max_length=100, blank=True)
 changes = models.JSONField(default=dict)
 ip_address = models.GenericIPAddressField(null=True, blank=True)
 user_agent = models.TextField(blank=True)
 created_at = models.DateTimeField(auto_now_add=True)
 def __str__(self): return f"{self.action} - {self.user} - {self.created_at}"