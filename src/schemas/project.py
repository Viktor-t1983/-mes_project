
from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    description: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    status: str = "active"

    class Config:
        from_attributes = True


class ProjectUpdate(BaseModel):
    # Add update fields here
    pass
    
    class Config:
        from_attributes = True

