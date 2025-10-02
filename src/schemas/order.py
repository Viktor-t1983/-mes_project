
from pydantic import BaseModel
from typing import Optional

class OrderBase(BaseModel):
    name: str
    description: str
    product_name: str
    quantity: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    status: str = "created"

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    # Add update fields here
    pass
    
    class Config:
        from_attributes = True

