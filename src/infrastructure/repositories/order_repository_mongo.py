from typing import Optional
from bson import ObjectId
from datetime import datetime

from ...domain.ports.order_repository import OrderRepository
from ...domain.models.order import Order, OrderItem
from ...domain.value_objects.order_status import OrderStatus
from ..db.mongo import get_db

def _to_domain(doc) -> Order:
    items = [OrderItem(**i) for i in doc["items"]]
    return Order(
        id=str(doc["_id"]),
        customer_id=doc["customer_id"],
        items=items,
        status=OrderStatus(doc["status"]),
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )

class OrderRepositoryMongo(OrderRepository):
    def __init__(self):
        self._db = get_db()
        self._col = self._db["orders"]

    async def create(self, order: Order) -> Order:
        payload = {
            "customer_id": order.customer_id,
            "items": [i.__dict__ for i in order.items],
            "status": order.status.value,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
        }
        result = await self._col.insert_one(payload)
        doc = await self._col.find_one({"_id": result.inserted_id})
        return _to_domain(doc)

    async def get_by_id(self, order_id: str) -> Optional[Order]:
        if not ObjectId.is_valid(order_id):
            return None
        doc = await self._col.find_one({"_id": ObjectId(order_id)})
        return _to_domain(doc) if doc else None

    async def update_status(self, order_id: str, status: OrderStatus) -> Order:
        if not ObjectId.is_valid(order_id):
            return None  # service decide error
        now = datetime.utcnow()
        result = await self._col.find_one_and_update(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": status.value, "updated_at": now}},
            return_document=True
        )
        return _to_domain(result) if result else None