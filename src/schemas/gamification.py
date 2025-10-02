from pydantic import BaseModel
from typing import Optional

class Achievement(BaseModel):
    id: int
    name: str
    description: str
    points: int

class LeaderboardEntry(BaseModel):
    rank: int
    employee_name: str
    points: int
    department: Optional[str] = None

class EmployeePerformance(BaseModel):
    employee_id: int
    total_points: int
    achievements: list
