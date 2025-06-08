from typing import Optional

class AppError(Exception):
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.message = message
        self.original_error = original_error

    def __str__(self) -> str:
        if self.original_error:
            return f"{self.message} (caused by: {str(self.original_error)})"
        return self.message

# Core application exceptions
class AuthenticationError(AppError):
    """Raised when authentication fails."""
    pass

class AuthorizationError(AppError):
    """Raised when a user is not authorized to perform an action."""
    pass

class ValidationError(AppError):
    """Raised when data validation fails."""
    pass

class NotFoundError(AppError):
    """Raised when a requested resource is not found."""
    pass

class ConflictError(AppError):
    """Raised when a resource conflict occurs (e.g., duplicate entry)."""
    pass

# OAuth/External Service exceptions
class OAuthError(AppError):
    """Base class for all OAuth-related errors."""
    pass

class InvalidTokenError(OAuthError):
    """Raised when an invalid or malformed token is encountered."""
    pass

class ProviderCommunicationError(OAuthError):
    """Raised when communication with an external provider fails."""
    pass

class MissingUserDataError(OAuthError):
    """Raised when required user data is missing from provider response."""
    pass

class OAuthStateError(OAuthError):
    """Raised when OAuth state validation fails (CSRF protection)."""
    pass

class OAuthProviderNotSupportedError(OAuthError):
    """Raised when an unsupported OAuth provider is requested."""
    pass

# Database exceptions
class DatabaseError(AppError):
    """Base class for database-related errors."""
    pass

class RecordNotFoundError(DatabaseError, NotFoundError):
    """Raised when a database record is not found."""
    pass

class DuplicateRecordError(DatabaseError, ConflictError):
    """Raised when a duplicate database record is detected."""
    pass

# Service layer exceptions
class ServiceError(AppError):
    """Base class for service layer errors."""
    pass

class RateLimitExceededError(ServiceError):
    """Raised when rate limits are exceeded."""
    pass

class ExternalServiceError(ServiceError):
    """Raised when an external service returns an error."""
    pass

ERROR_STATUS_CODES = {
    # App Errors
    AuthenticationError: 401,
    AuthorizationError: 403,
    ValidationError: 400,
    NotFoundError: 404,
    ConflictError: 409,
    
    # OAuth errors
    OAuthError: 400,
    InvalidTokenError: 401,
    ProviderCommunicationError: 502,
    MissingUserDataError: 400,
    OAuthStateError: 400,
    OAuthProviderNotSupportedError: 400,
    
    # Database errors
    DatabaseError: 500,
    RecordNotFoundError: 404,
    DuplicateRecordError: 409,
    
    # Service errors
    ServiceError: 500,
    RateLimitExceededError: 429,
    ExternalServiceError: 503,
}

def get_http_status_code(error: AppError) -> int:
    return ERROR_STATUS_CODES.get(type(error), 500)
