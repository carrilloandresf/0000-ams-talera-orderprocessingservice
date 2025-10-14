from pydantic import BaseModel
from datetime import datetime
from typing import List
from .order_create import OrderItemIn

class OrderOut(BaseModel):
    id: str
    customer_id: str
    items: List[OrderItemIn]
    status: str
    created_at: datetime
    updated_at: datetime