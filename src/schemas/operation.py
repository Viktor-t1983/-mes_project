
from pydantic import BaseModel
from typing import Optional

class OperationBase(BaseModel):
    manufacturing_order_id: int
    operation_number: str
    name: str
    description: str
    planned_duration: int

class OperationCreate(OperationBase):
    pass

class Operation(OperationBase):
    id: int
    status: str = "pending"

    class Config:
        from_attributes = True
