import uuid
from django.db import models
class PermissionCategory(models.Model):
 class Meta:
 db_table = 'auth_permission_categories'
 verbose_name = 'Permission Category'
 verbose_name_plural = 'Permission Categories'
 ordering = ['order', 'name']
 id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
 name = models.CharField(max_length=100, unique=True)
 code = models.CharField(max_length=50, unique=True)
 description = models.TextField(blank=True)
 icon = models.CharField(max_length=50, blank=True)
 order = models.IntegerField(default=0)
 is_system = models.BooleanField(default=False)
 parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)
 def __str__(self):
 return self.name
 def get_full_path(self):
 if self.parent:
 return f"{self.parent.get_full_path()} > {self.name}"
 return self.name