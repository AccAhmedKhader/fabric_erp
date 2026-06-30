"""
Global constants for the application.
"""


class UserRoles:
    """User role constants."""
    ADMINISTRATOR = 'System Administrator'
    ACCOUNTANT = 'Accountant'
    SALES_MANAGER = 'Sales Manager'
    INVENTORY_MANAGER = 'Inventory Manager'
    PURCHASING_MANAGER = 'Purchasing Manager'
    HR_MANAGER = 'HR Manager'
    USER = 'User'


class Permissions:
    """Permission code constants."""
    VIEW_DASHBOARD = 'view_dashboard'
    VIEW_AUDIT_LOG = 'view_audit_log'
    MANAGE_USERS = 'manage_users'
    MANAGE_ROLES = 'manage_roles'
    MANAGE_PERMISSIONS = 'manage_permissions'
    VIEW_SYSTEM_SETTINGS = 'view_system_settings'
    MANAGE_SYSTEM_SETTINGS = 'manage_system_settings'
    VIEW_COMPANIES = 'view_companies'
    MANAGE_COMPANIES = 'manage_companies'
    VIEW_BRANCHES = 'view_branches'
    MANAGE_BRANCHES = 'manage_branches'


class Modules:
    """Module name constants."""
    AUTHENTICATION = 'authentication'
    COMPANY = 'company'
    SETTINGS = 'settings'
    ACCOUNTING = 'accounting'
    INVENTORY = 'inventory'
    SALES = 'sales'
    PURCHASING = 'purchasing'
    HR = 'hr'