
from pydantic import BaseModel
from typing import Optional

class ManufacturingOrderBase(BaseModel):
    order_number: str
    product_name: str
    product_code: str
    quantity: int

class ManufacturingOrderCreate(ManufacturingOrderBase):
    pass

class ManufacturingOrder(ManufacturingOrderBase):
    id: int
    status: str = "planned"

    class Config:
        from_attributes = True
