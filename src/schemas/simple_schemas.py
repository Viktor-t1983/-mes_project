from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SimpleProjectCreate(BaseModel):
    name: str
    description: str

class SimpleProject(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

class SimpleOperationCreate(BaseModel):
    name: str
    description: str
    operation_type: Optional[str] = "machining"
    duration_minutes: Optional[int] = 60
    cost: Optional[float] = 0.0

class SimpleOperation(BaseModel):
    id: int
    name: str
    description: str
    operation_type: str
    duration_minutes: int
    cost: float
    created_at: datetime

    class Config:
        from_attributes = True
