"""Simulated AWS clients used for logging side-effects."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def _log_simulated_call(service: str, action: str, payload: Dict[str, Any]) -> None:
    logger.info(
        "Simulated AWS call",
        extra={
            "service": service,
            "action": action,
            "payload": json.dumps(payload, default=str),
        },
    )


def publish_eventbridge_event(event_type: str, detail: Dict[str, Any]) -> None:
    """Pretend to publish an event to Amazon EventBridge."""
    payload = {
        "detail-type": event_type,
        "detail": detail,
        "time": datetime.utcnow().isoformat(),
    }
    _log_simulated_call("eventbridge", "put_events", payload)


def upload_order_manifest(order_id: str, content: Dict[str, Any]) -> None:
    """Pretend to upload an order manifest to S3."""
    payload = {"bucket": "orders-manifest", "key": f"{order_id}.json", "body": content}
    _log_simulated_call("s3", "put_object", payload)
