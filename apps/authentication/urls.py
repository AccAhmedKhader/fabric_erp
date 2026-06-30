"""
URL configuration for authentication app.
"""

from django.urls import path
from .views import auth_views, user_views, role_views, permission_views, health_views

app_name = 'authentication'

urlpatterns = [
    # Splash and Login
    path('', auth_views.splash, name='splash'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('dashboard/', auth_views.dashboard, name='dashboard'),

    # Password Management
    path('forgot-password/', auth_views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', auth_views.reset_password, name='reset_password'),
    path('change-password/', auth_views.change_password, name='change_password'),

    # Email Verification
    path('verify-email/<uidb64>/<token>/', auth_views.verify_email, name='verify_email'),
    path('resend-verification/', auth_views.resend_verification, name='resend_verification'),
    path('account-locked/', auth_views.account_locked, name='account_locked'),

    # User Management
    path('users/', user_views.user_list, name='user_list'),
    path('users/add/', user_views.user_add, name='user_add'),
    path('users/<uuid:user_id>/edit/', user_views.user_edit, name='user_edit'),
    path('users/<uuid:user_id>/delete/', user_views.user_delete, name='user_delete'),
    path('users/<uuid:user_id>/toggle-active/', user_views.user_toggle_active, name='user_toggle_active'),

    # Role Management
    path('roles/', role_views.role_list, name='role_list'),
    path('roles/add/', role_views.role_add, name='role_add'),
    path('roles/<uuid:role_id>/edit/', role_views.role_edit, name='role_edit'),
    path('roles/<uuid:role_id>/delete/', role_views.role_delete, name='role_delete'),
    path('roles/<uuid:role_id>/assign-permissions/', role_views.role_assign_permissions, name='role_assign_permissions'),

    # Permission Management
    path('permissions/', permission_views.permission_list, name='permission_list'),
    path('permissions/add/', permission_views.permission_add, name='permission_add'),
    path('permissions/<uuid:permission_id>/delete/', permission_views.permission_delete, name='permission_delete'),

    # Health Checks
    path('health/', health_views.health_check, name='health'),
    path('health/readiness/', health_views.readiness_check, name='readiness'),
    path('health/liveness/', health_views.liveness_check, name='liveness'),
    path('health/metrics/', health_views.metrics, name='metrics'),
]