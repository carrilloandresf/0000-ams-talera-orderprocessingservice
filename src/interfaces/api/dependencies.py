"""Dependency providers for FastAPI routers."""
from ...application.services.order_service import OrderService
from ...infrastructure.repositories.order_repository_mongo import OrderRepositoryMongo


def get_order_service() -> OrderService:
    repo = OrderRepositoryMongo()
    return OrderService(repo=repo)
