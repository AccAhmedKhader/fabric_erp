"""
Custom exceptions for the application.
"""


class FabricERPException(Exception):
    """Base exception for FabricERP application."""
    pass


class AuthenticationError(FabricERPException):
    """Exception raised for authentication errors."""
    pass


class PermissionDeniedError(FabricERPException):
    """Exception raised for permission errors."""
    pass


class UserNotFoundError(FabricERPException):
    """Exception raised when a user is not found."""
    pass


class RoleNotFoundError(FabricERPException):
    """Exception raised when a role is not found."""
    pass


class PermissionNotFoundError(FabricERPException):
    """Exception raised when a permission is not found."""
    pass


class InvalidTokenError(FabricERPException):
    """Exception raised for invalid tokens."""
    pass


class AccountLockedError(FabricERPException):
    """Exception raised when an account is locked."""
    pass


class CompanyNotFoundError(FabricERPException):
    """Exception raised when a company is not found."""
    pass


class BranchNotFoundError(FabricERPException):
    """Exception raised when a branch is not found."""
    pass


class ValidationError(FabricERPException):
    """Exception raised for validation errors."""
    pass


class DuplicateError(FabricERPException):
    """Exception raised for duplicate entries."""
    pass


class DatabaseError(FabricERPException):
    """Exception raised for database errors."""
    pass


class ServiceError(FabricERPException):
    """Exception raised for service layer errors."""
    pass


class ConfigurationError(FabricERPException):
    """Exception raised for configuration errors."""
    pass