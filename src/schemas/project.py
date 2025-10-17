from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"  # ← Обязательное поле со значением по умолчанию

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
