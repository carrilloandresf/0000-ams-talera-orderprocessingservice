"""MongoDB client helpers."""
from __future__ import annotations

import logging
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from ...core.config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_client() -> AsyncIOMotorClient:
    """Return a cached Motor client instance."""
    uri = (
        f"mongodb://{settings.mongo_user}:{settings.mongo_password}"
        f"@{settings.mongo_host}:{settings.mongo_port}/"
        f"?authSource={settings.mongo_auth_source}"
    )
    logger.debug("Creating MongoDB client", extra={"mongo_uri": uri})
    return AsyncIOMotorClient(uri)


def get_database() -> AsyncIOMotorDatabase:
    """Return the configured database handle."""
    client = get_client()
    db = client[settings.mongo_db]
    logger.debug("Obtained MongoDB database", extra={"database": settings.mongo_db})
    return db
