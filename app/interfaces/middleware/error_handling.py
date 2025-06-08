import logging
from typing import Any, Dict

from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.exceptions import (
    AppError,
    OAuthError,
    get_http_status_code,
)

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        try:
            await self.app(scope, receive, send)
        except AppError as e:
            await self._handle_application_error(e, scope, receive, send)
        except Exception as e:
            await self._handle_unexpected_error(e, scope, receive, send)

    async def _handle_application_error(
        self, error: AppError, scope: Scope, receive: Receive, send: Send
    ) -> None:
        """Handle all known application errors with proper status codes."""
        status_code = get_http_status_code(error)
        error_detail = self._build_error_detail(error)

        logger.warning(
            "Application error occurred",
            exc_info=error,
            extra={
                "error_type": error.__class__.__name__,
                "status_code": status_code,
                "scope": self._sanitize_scope(scope),
            },
        )

        response = JSONResponse(
            status_code=status_code,
            content=error_detail,
        )
        await response(scope, receive, send)

    async def _handle_unexpected_error(
        self, error: Exception, scope: Scope, receive: Receive, send: Send
    ) -> None:
        """Handle unexpected errors with 500 status and generic message."""
        logger.error(
            "Unexpected server error",
            exc_info=error,
            extra={"scope": self._sanitize_scope(scope)},
        )

        response = JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
            },
        )
        await response(scope, receive, send)

    def _build_error_detail(self, error: AppError) -> Dict[str, Any]:
        detail = {
            "error": error.__class__.__name__,
            "message": str(error),
        }

        if isinstance(error, OAuthError) and error.original_error:
            detail["details"] = str(error.original_error)

        return detail

    def _sanitize_scope(self, scope: Scope) -> Dict[str, Any]:
        return {
            "type": scope["type"],
            "path": scope.get("path"),
            "method": scope.get("method"),
            "headers": {k.decode(): v.decode() for k, v in scope.get("headers", [])},
            "query_string": scope.get("query_string", b"").decode(),
        }
