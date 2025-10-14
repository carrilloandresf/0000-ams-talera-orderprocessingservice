"""HTTP endpoints for order resources."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ...application.dto.order_create import OrderCreateIn
from ...application.dto.order_read import OrderOut
from ...application.dto.order_update_status import OrderStatusUpdateIn
from ...application.services.order_service import OrderService
from ...domain.models.order import Order
from .dependencies import get_order_service

router = APIRouter(prefix="/orders", tags=["orders"])


def _to_response(order: Order) -> OrderOut:
    return OrderOut(
        id=order.id or "",
        customer_id=order.customer_id,
        items=[item.__dict__ for item in order.items],
        status=order.status.value,
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


@router.post("", response_model=OrderOut, status_code=201)
async def create_order(
    payload: OrderCreateIn,
    svc: OrderService = Depends(get_order_service),
) -> OrderOut:
    order = await svc.create_order(
        customer_id=payload.customer_id,
        items=[item.model_dump() for item in payload.items],
    )
    return _to_response(order)


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: str, svc: OrderService = Depends(get_order_service)) -> OrderOut:
    order = await svc.get_order(order_id)
    return _to_response(order)


@router.patch("/{order_id}", response_model=OrderOut)
async def update_status(
    order_id: str,
    payload: OrderStatusUpdateIn,
    svc: OrderService = Depends(get_order_service),
) -> OrderOut:
    order = await svc.update_order_status(order_id, payload.status)
    return _to_response(order)
