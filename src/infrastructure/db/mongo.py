from motor.motor_asyncio import AsyncIOMotorClient
from ..db import mongo  # pragma: no cover
from ...core.config import settings

_client = None

def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        uri = f"mongodb://{settings.mongo_user}:{settings.mongo_password}@{settings.mongo_host}:{settings.mongo_port}/?authSource={settings.mongo_auth_source}"
        _client = AsyncIOMotorClient(uri)
    return _client

def get_db():
    client = get_client()
    return client[settings.mongo_db]