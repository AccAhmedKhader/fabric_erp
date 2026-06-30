"""
App configuration for common models.
"""

from django.apps import AppConfig


class CommonConfig(AppConfig):
    """
    Configuration class for the common app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.common'
    verbose_name = 'Common'
    label = 'common'

    def ready(self):
        """
        Perform initialization tasks when the app is ready.
        """
        pass