from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DefectReportBase(BaseModel):
    description: str
    severity: str = "low"
    status: str = "open"

class DefectReportCreate(DefectReportBase):
    pass

class DefectReportUpdate(DefectReportBase):
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None

class DefectReport(DefectReportBase):
    id: int
    
    class Config:
        from_attributes = True
