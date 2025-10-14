from fastapi import APIRouter, Depends
from ...application.dto.order_create import OrderCreateIn
from ...application.dto.order_read import OrderOut
from ...application.dto.order_update_status import OrderStatusUpdateIn
from .dependencies import get_order_service
from ...application.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderOut, status_code=201)
async def create_order(payload: OrderCreateIn, svc: OrderService = Depends(get_order_service)):
    order = await svc.create_order(customer_id=payload.customer_id, items=[i.model_dump() for i in payload.items])
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "items": [i.__dict__ for i in order.items],
        "status": order.status.value,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
    }

@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: str, svc: OrderService = Depends(get_order_service)):
    order = await svc.get_order(order_id)
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "items": [i.__dict__ for i in order.items],
        "status": order.status.value,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
    }

@router.patch("/{order_id}", response_model=OrderOut)
async def update_status(order_id: str, payload: OrderStatusUpdateIn, svc: OrderService = Depends(get_order_service)):
    order = await svc.update_order_status(order_id, payload.status)
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "items": [i.__dict__ for i in order.items],
        "status": order.status.value,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
    }