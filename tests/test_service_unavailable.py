"""Tests for service unavailable scenarios."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest
from pymongo.errors import PyMongoError

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.application.services.order_service import OrderService
from src.infrastructure.repositories.order_repository_mongo import OrderRepositoryMongo
from src.interfaces.api.dependencies import get_order_service
from src.main import app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class _FailingCollection:
    async def insert_one(self, payload):  # type: ignore[override]
        raise PyMongoError("boom")


def _failing_service() -> OrderService:
    repo = OrderRepositoryMongo.__new__(OrderRepositoryMongo)
    repo._collection = _FailingCollection()  # type: ignore[attr-defined]
    return OrderService(repo=repo)


@pytest.mark.anyio("asyncio")
async def test_create_order_returns_503_when_database_unavailable():
    app.dependency_overrides[get_order_service] = _failing_service

    body = json.dumps(
        {
            "customer_id": "cust-1",
            "items": [
                {
                    "sku": "SKU-1",
                    "quantity": 1,
                    "unit_price": 10.0,
                }
            ],
        }
    ).encode()

    messages: List[Dict[str, Any]] = []
    body_sent = False

    async def receive() -> Dict[str, Any]:
        nonlocal body_sent
        if not body_sent:
            body_sent = True
            return {"type": "http.request", "body": body, "more_body": False}
        return {"type": "http.disconnect"}

    async def send(message: Dict[str, Any]) -> None:
        messages.append(message)

    scope: Dict[str, Any] = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "method": "POST",
        "path": "/orders",
        "raw_path": b"/orders",
        "query_string": b"",
        "headers": [(b"content-type", b"application/json")],
        "client": ("testclient", 12345),
        "server": ("testserver", 80),
    }

    await app(scope, receive, send)

    status = next(msg["status"] for msg in messages if msg["type"] == "http.response.start")
    body_bytes = b"".join(msg.get("body", b"") for msg in messages if msg["type"] == "http.response.body")

    assert status == 503
    assert json.loads(body_bytes) == {"error": "Database unavailable"}

    app.dependency_overrides.pop(get_order_service, None)
