"""
Permission management forms.
"""

from django import forms
from ..models import EnterprisePermission


class PermissionForm(forms.ModelForm):
    """Permission creation form."""

    class Meta:
        model = EnterprisePermission
        fields = ['django_permission', 'category', 'permission_type', 'is_system', 'description']
        widgets = {
            'django_permission': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'permission_type': forms.Select(attrs={'class': 'form-control'}),
            'is_system': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }