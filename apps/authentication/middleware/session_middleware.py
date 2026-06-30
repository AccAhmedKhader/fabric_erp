"""
Session timeout middleware for automatic session expiration.
"""

from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


class SessionTimeoutMiddleware:
    """
    Middleware that checks for session expiration and handles timeout.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key
            if session_key:
                from ..models import UserSession
                try:
                    user_session = UserSession.objects.get(
                        session_key=session_key,
                        is_active=True
                    )

                    if user_session.is_expired():
                        from django.contrib.auth import logout
                        logout(request)
                        request.session.flush()
                        return redirect(reverse('authentication:login') + '?expired=1')

                    user_session.last_activity = timezone.now()
                    user_session.save(update_fields=['last_activity'])

                except UserSession.DoesNotExist:
                    pass

        response = self.get_response(request)
        return response