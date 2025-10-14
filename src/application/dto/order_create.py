from pydantic import BaseModel, Field, conlist, conint, confloat

class OrderItemIn(BaseModel):
    sku: str = Field(min_length=1)
    quantity: conint(gt=0)
    unit_price: confloat(gt=0)

class OrderCreateIn(BaseModel):
    customer_id: str = Field(min_length=1)
    items: conlist(OrderItemIn, min_items=1)