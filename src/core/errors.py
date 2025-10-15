"""Custom error hierarchy and FastAPI handlers."""
from __future__ import annotations

from fastapi import Request, status
from fastapi.responses import JSONResponse


class DomainError(Exception):
    """Base class for domain level errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(DomainError):
    """Raised when a resource cannot be located."""


class ConflictError(DomainError):
    """Raised on domain conflicts (duplicates, invalid transitions, etc.)."""


class BadRequestError(DomainError):
    """Raised when the input data is invalid."""


class ServiceUnavailableError(DomainError):
    """Raised when downstream dependencies are unavailable."""


async def domain_error_handler(_: Request, exc: DomainError) -> JSONResponse:
    code_map = {
        NotFoundError: status.HTTP_404_NOT_FOUND,
        ConflictError: status.HTTP_409_CONFLICT,
        BadRequestError: status.HTTP_400_BAD_REQUEST,
        ServiceUnavailableError: status.HTTP_503_SERVICE_UNAVAILABLE,
        DomainError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    }
    for cls, code in code_map.items():
        if isinstance(exc, cls):
            return JSONResponse(status_code=code, content={"error": exc.message})
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
