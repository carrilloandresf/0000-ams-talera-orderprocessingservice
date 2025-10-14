"""Application service orchestrating order use-cases."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import List

from ...core.errors import BadRequestError, NotFoundError
from ...domain.models.order import Order, OrderItem
from ...domain.ports.order_repository import OrderRepository
from ...domain.value_objects.order_status import OrderStatus
from ...infrastructure.aws.simulated_clients import (
    publish_eventbridge_event,
    upload_order_manifest,
)

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, repo: OrderRepository):
        self._repo = repo

    async def create_order(self, customer_id: str, items: List[dict]) -> Order:
        logger.info("Creating order", extra={"customer_id": customer_id})
        if not items:
            logger.error("Attempted to create order without items", extra={"customer_id": customer_id})
            raise BadRequestError("Order must contain at least one item")

        domain_items = [OrderItem(**item) for item in items]
        order = Order(
            customer_id=customer_id,
            items=domain_items,
            status=OrderStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        created = await self._repo.create(order)
        logger.info("Order created", extra={"order_id": created.id})

        upload_order_manifest(created.id or "unknown", {
            "order_id": created.id,
            "customer_id": created.customer_id,
            "items": [item.__dict__ for item in created.items],
        })
        publish_eventbridge_event(
            "OrderCreated",
            {
                "orderId": created.id,
                "customerId": created.customer_id,
                "status": created.status.value,
            },
        )

        return created

    async def get_order(self, order_id: str) -> Order:
        logger.debug("Fetching order", extra={"order_id": order_id})
        order = await self._repo.get_by_id(order_id)
        if not order:
            logger.warning("Order not found", extra={"order_id": order_id})
            raise NotFoundError("Order not found")
        return order

    async def update_order_status(self, order_id: str, status_str: str) -> Order:
        logger.info("Updating order status", extra={"order_id": order_id, "status": status_str})
        try:
            status = OrderStatus(status_str)
        except ValueError as exc:
            logger.error("Invalid status supplied", extra={"order_id": order_id, "status": status_str})
            raise BadRequestError("Invalid status value") from exc

        updated = await self._repo.update_status(order_id, status)
        if not updated:
            logger.warning("Order not found for status update", extra={"order_id": order_id})
            raise NotFoundError("Order not found")

        publish_eventbridge_event(
            "OrderStatusChanged",
            {
                "orderId": updated.id,
                "status": updated.status.value,
            },
        )
        return updated
