"""MongoDB implementation for :class:`OrderRepository`."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from ...domain.models.order import Order, OrderItem
from ...domain.ports.order_repository import OrderRepository
from ...domain.value_objects.order_status import OrderStatus
from ..db.mongo import get_database

logger = logging.getLogger(__name__)


def _to_domain(doc: dict) -> Order:
    items = [OrderItem(**item) for item in doc["items"]]
    return Order(
        id=str(doc["_id"]),
        customer_id=doc["customer_id"],
        items=items,
        status=OrderStatus(doc["status"]),
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )


def _to_document(order: Order) -> dict:
    return {
        "customer_id": order.customer_id,
        "items": [item.__dict__ for item in order.items],
        "status": order.status.value,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
    }


class OrderRepositoryMongo(OrderRepository):
    """MongoDB backed repository for orders."""

    def __init__(self) -> None:
        database = get_database()
        self._collection: AsyncIOMotorCollection = database["orders"]

    async def create(self, order: Order) -> Order:
        logger.info("Persisting new order", extra={"customer_id": order.customer_id})
        payload = _to_document(order)
        result = await self._collection.insert_one(payload)
        logger.debug("Order persisted", extra={"order_id": str(result.inserted_id)})
        doc = await self._collection.find_one({"_id": result.inserted_id})
        return _to_domain(doc)

    async def get_by_id(self, order_id: str) -> Optional[Order]:
        if not ObjectId.is_valid(order_id):
            logger.warning("Invalid ObjectId received", extra={"order_id": order_id})
            return None
        doc = await self._collection.find_one({"_id": ObjectId(order_id)})
        if doc:
            logger.debug("Order retrieved", extra={"order_id": order_id})
            return _to_domain(doc)
        logger.info("Order not found", extra={"order_id": order_id})
        return None

    async def update_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        if not ObjectId.is_valid(order_id):
            logger.warning("Invalid ObjectId received for update", extra={"order_id": order_id})
            return None

        now = datetime.utcnow()
        doc = await self._collection.find_one_and_update(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": status.value, "updated_at": now}},
            return_document=True,
        )

        if not doc:
            logger.info("Order not found for status update", extra={"order_id": order_id})
            return None

        logger.info(
            "Order status updated",
            extra={"order_id": order_id, "status": status.value},
        )
        return _to_domain(doc)
