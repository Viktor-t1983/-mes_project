from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    machine_id: Optional[int] = None
    action: str
    ip_address: str
    data_snapshot: str

class AuditLog(AuditLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
