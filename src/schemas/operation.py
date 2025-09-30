from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any

class OperationStart(BaseModel):
    mo_id: int
    employee_qr: str
    workcenter_id: str

class OperationPause(BaseModel):
    operation_id: int
    reason: str

class OperationComplete(BaseModel):
    operation_id: int
    employee_qr: str  # для подтверждения

class OperationBase(BaseModel):
    operation_number: str
    name: str
    workcenter_id: str
    operation_type: str
    description: Optional[str] = None
    planned_duration: Optional[float] = None
    status: str = "pending"
    notes: Optional[str] = None
    pause_events: Optional[Dict[str, Any]] = None
    qr_code: Optional[str] = None

class OperationCreate(OperationBase):
    manufacturing_order_id: int
    assigned_employee_id: Optional[int] = None

class OperationUpdate(BaseModel):
    operation_number: Optional[str] = None
    name: Optional[str] = None
    workcenter_id: Optional[str] = None
    operation_type: Optional[str] = None
    description: Optional[str] = None
    planned_duration: Optional[float] = None
    actual_duration: Optional[float] = None
    status: Optional[str] = None
    assigned_employee_id: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    quality_check_passed: Optional[bool] = None
    pause_events: Optional[Dict[str, Any]] = None
    qr_code: Optional[str] = None
    notes: Optional[str] = None

class Operation(OperationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    manufacturing_order_id: int
    assigned_employee_id: Optional[int] = None
    actual_duration: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    quality_check_passed: Optional[bool] = None
    created_at: datetime
    
