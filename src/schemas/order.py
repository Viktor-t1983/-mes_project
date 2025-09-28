from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .project import Project

class OrderBase(BaseModel):
    project_id: int
    name: str
    description: str
    quantity: int = 1
    status: str = "draft"
    priority: str = "medium"
    deadline: Optional[datetime] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[datetime] = None

class Order(OrderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class OrderWithProject(Order):
    project: Project
