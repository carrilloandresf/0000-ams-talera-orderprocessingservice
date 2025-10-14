from typing import Optional
from datetime import datetime
from ...domain.ports.order_repository import OrderRepository
from ...domain.models.order import Order, OrderItem
from ...domain.value_objects.order_status import OrderStatus
from ...core.errors import NotFoundError, BadRequestError

class OrderService:
    def __init__(self, repo: OrderRepository):
        self._repo = repo

    async def create_order(self, customer_id: str, items: list[dict]) -> Order:
        if not items:
            raise BadRequestError("Order must contain at least one item")
        domain_items = [OrderItem(**i) for i in items]
        order = Order(
            customer_id=customer_id,
            items=domain_items,
            status=OrderStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return await self._repo.create(order)

    async def get_order(self, order_id: str) -> Order:
        order = await self._repo.get_by_id(order_id)
        if not order:
            raise NotFoundError("Order not found")
        return order

    async def update_order_status(self, order_id: str, status_str: str) -> Order:
        try:
            status = OrderStatus(status_str)
        except ValueError:
            raise BadRequestError("Invalid status value")

        updated = await self._repo.update_status(order_id, status)
        if not updated:
            raise NotFoundError("Order not found")
        return updated