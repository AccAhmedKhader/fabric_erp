"""
Context processors for providing company information and app settings.
"""

from django.conf import settings


def company_info(request):
    """
    Provide company information to all templates.
    """
    return {
        'company_name': getattr(settings, 'COMPANY_NAME', 'FabricERP'),
        'company_phone': getattr(settings, 'COMPANY_PHONE', ''),
        'company_email': getattr(settings, 'COMPANY_EMAIL', ''),
        'company_address': getattr(settings, 'COMPANY_ADDRESS', ''),
    }


def app_version(request):
    """
    Provide application version and environment to all templates.
    """
    return {
        'app_version': getattr(settings, 'APP_VERSION', '1.0.0'),
        'environment': getattr(settings, 'ENVIRONMENT', 'development'),
        'debug': getattr(settings, 'DEBUG', False),
    }


def user_session(request):
    """
    Provide user session information to all templates.
    """
    context = {}

    if request.user.is_authenticated:
        context['user'] = request.user
        context['user_full_name'] = request.user.get_full_name()
        context['user_last_login'] = request.user.last_login

        if hasattr(request.user, 'profile'):
            context['user_avatar'] = request.user.profile.get_avatar_url()

    return context