from pydantic import BaseModel, Any
from typing import Optional

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    role: str
    qr_code: Optional[str] = None
    allowed_workcenters: Optional[Any] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    allowed_workcenters: Optional[Any] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True
