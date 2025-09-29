from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class DefectReportBase(BaseModel):
    defect_type: str
    defect_description: str
    severity: str = "medium"
    quantity_affected: int = 1
    corrective_action: Optional[str] = None
    status: str = "reported"

class DefectReportCreate(DefectReportBase):
    manufacturing_order_id: int
    operation_id: Optional[int] = None
    reported_by: int

class DefectReportUpdate(BaseModel):
    defect_type: Optional[str] = None
    defect_description: Optional[str] = None
    severity: Optional[str] = None
    quantity_affected: Optional[int] = None
    corrective_action: Optional[str] = None
    status: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None

class DefectReport(DefectReportBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    manufacturing_order_id: int
    operation_id: Optional[int] = None
    reported_by: int
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    created_at: datetime
