from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OperationBase(BaseModel):
    name: str
    description: Optional[str] = None
    planned_duration: int
    qr_code: str

class OperationCreate(OperationBase):
    pass

class OperationUpdate(BaseModel):
    status: Optional[str] = None
    actual_duration: Optional[int] = None
    employee_id: Optional[int] = None
    defect_reason: Optional[str] = None

class Operation(OperationBase):
    id: int
    status: str
    actual_duration: Optional[int] = None
    employee_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    defect_reason: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
