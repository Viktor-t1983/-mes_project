
from pydantic import BaseModel
from typing import Optional

class DefectReportBase(BaseModel):
    manufacturing_order_id: int
    reported_by: int
    defect_type: str
    defect_description: str
    severity: str

class DefectReportCreate(DefectReportBase):
    pass

class DefectReport(DefectReportBase):
    id: int
    status: str = "reported"

    class Config:
        from_attributes = True
