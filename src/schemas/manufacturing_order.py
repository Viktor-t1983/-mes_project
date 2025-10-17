from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ManufacturingOrderBase(BaseModel):
    project_id: int
    part_number: str
    status: str = "planned"

class ManufacturingOrderCreate(ManufacturingOrderBase):
    pass

class ManufacturingOrderResponse(ManufacturingOrderBase):
    id: int
    current_operation_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
