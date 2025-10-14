from fastapi import FastAPI
from .core.logging_config import configure_logging
from .core.errors import DomainError, domain_error_handler
from .interfaces.api.routers_orders import router as orders_router

configure_logging()
app = FastAPI(title="Order Processing Service", version="1.0.0")

# Exception mapping (Domain -> HTTP)
app.add_exception_handler(DomainError, domain_error_handler)

# Routers
app.include_router(orders_router)

@app.get("/health")
async def health():
    return {"status": "ok"}