"""FastAPI application entry-point."""
from __future__ import annotations

from fastapi import FastAPI

from .core.errors import DomainError, domain_error_handler
from .core.logging_config import configure_logging
from .interfaces.api.routers_orders import router as orders_router

configure_logging()

app = FastAPI(
    title="Order Processing Service",
    version="1.0.0",
    description=(
        "Serverless-friendly order processing API. It exposes operations to create, read "
        "and update orders while logging simulated AWS interactions for educational purposes."
    ),
)

# Exception mapping (Domain -> HTTP)
app.add_exception_handler(DomainError, domain_error_handler)

# Routers
app.include_router(orders_router)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    """Lightweight health endpoint used by orchestration layers."""
    return {"status": "ok"}
