from pydantic import BaseModel, Field

class OrderStatusUpdateIn(BaseModel):
    status: str = Field(pattern="^(PENDING|PAID|SHIPPED|DELIVERED|CANCELED)$")