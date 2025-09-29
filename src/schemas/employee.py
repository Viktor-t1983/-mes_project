from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    qr_code: str
    first_name: str
    last_name: str
    position: str
    department: str
    qualifications: Optional[str] = None
    is_active: bool = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    qr_code: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    qualifications: Optional[str] = None
    is_active: Optional[bool] = None

class Employee(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
