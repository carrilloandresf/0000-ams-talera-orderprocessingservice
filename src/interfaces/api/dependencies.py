from ..api import dependencies  # pragma: no cover
from ...infrastructure.repositories.order_repository_mongo import OrderRepositoryMongo
from ...application.services.order_service import OrderService

def get_order_service() -> OrderService:
    repo = OrderRepositoryMongo()
    return OrderService(repo=repo)