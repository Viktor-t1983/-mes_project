from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderBase(BaseModel):
    name: str
    product_name: str
    quantity: int
    project_id: int

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
