from pydantic import BaseModel
from typing import Optional

class OperationStart(BaseModel):
    employee_qr: str
    part_number: str
    workcenter_id: str

class OperationPause(BaseModel):
    operation_id: int
    reason: str

class OperationComplete(BaseModel):
    operation_id: int
    employee_qr: str

class OperationResponse(BaseModel):
    status: str
    operation_id: Optional[int] = None
    event_id: Optional[int] = None
