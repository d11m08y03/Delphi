class AppError(Exception):
    """Base class for all application-specific errors."""
    pass

class NotFoundError(AppError):
    """Raised when a requested resource is not found."""
    pass

class AuthenticationError(AppError):
    """Raised when authentication fails."""
    pass

class ValidationError(AppError):
    """Raised when data validation fails."""
    pass
