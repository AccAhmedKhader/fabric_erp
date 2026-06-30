"""
App configuration for authentication app.
"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Configuration class for the authentication app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentication'
    verbose_name = 'Authentication & Authorization'
    label = 'authentication'

    def ready(self):
        """
        Perform initialization tasks when the app is ready.
        """
        # Import signals
        import apps.authentication.signals  # noqa