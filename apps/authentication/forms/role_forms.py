"""
Role management forms.
"""

from django import forms
from ..models import Role


class RoleForm(forms.ModelForm):
    """Role creation form."""
    class Meta:
        model = Role
        fields = ['name', 'description', 'is_system']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_system': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RoleEditForm(forms.ModelForm):
    """Role edit form."""
    class Meta:
        model = Role
        fields = ['name', 'description', 'is_system']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_system': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }