from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
import json

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    role: str  # "operator", "master", "inspector"
    allowed_workcenters: List[str] = []  # ["cnc1", "laser2"]
    qr_code: str
    is_active: bool = True

class EmployeeCreate(EmployeeBase):
    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        # Преобразуем список в JSON строку для БД
        if isinstance(data.get('allowed_workcenters'), list):
            data['allowed_workcenters'] = json.dumps(data['allowed_workcenters'], ensure_ascii=False)
        return data

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    allowed_workcenters: Optional[List[str]] = None
    qr_code: Optional[str] = None
    is_active: Optional[bool] = None

class Employee(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Для обратной совместимости
    @classmethod
    def validate_allowed_workcenters(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
        