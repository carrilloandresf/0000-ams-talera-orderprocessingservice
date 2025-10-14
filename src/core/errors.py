from fastapi import Request, status
from fastapi.responses import JSONResponse

class DomainError(Exception):
    def __init__(self, message: str):
        self.message = message

class NotFoundError(DomainError): ...
class ConflictError(DomainError): ...
class BadRequestError(DomainError): ...

async def domain_error_handler(_: Request, exc: DomainError):
    code_map = {
        NotFoundError: status.HTTP_404_NOT_FOUND,
        ConflictError: status.HTTP_409_CONFLICT,
        BadRequestError: status.HTTP_400_BAD_REQUEST,
        DomainError: status.HTTP_422_UNPROCESSABLE_ENTITY
    }
    for cls, code in code_map.items():
        if isinstance(exc, cls):
            return JSONResponse(status_code=code, content={"error": exc.message})
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})