from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OperationBase(BaseModel):
    name: str
    status: str = "pending"

class OperationCreate(OperationBase):
    pass

class OperationUpdate(OperationBase):
    name: Optional[str] = None

class OperationPause(BaseModel):
    reason: str

class Operation(OperationBase):
    id: int
    
    class Config:
        from_attributes = True
