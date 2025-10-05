from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MachineBase(BaseModel):
    name: str
    type: str
    location: Optional[str] = None
    technical_docs: Optional[str] = None

class MachineCreate(MachineBase):
    machine_token: str

class Machine(MachineBase):
    id: int
    status: str
    last_heartbeat: datetime

    class Config:
        from_attributes = True
