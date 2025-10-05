from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AchievementBase(BaseModel):
    name: str
    description: str
    points: int

class AchievementCreate(AchievementBase):
    pass

class Achievement(AchievementBase):
    id: int

    class Config:
        from_attributes = True

class EmployeeAchievementBase(BaseModel):
    employee_id: int
    achievement_id: int

class EmployeeAchievementCreate(EmployeeAchievementBase):
    pass

class EmployeeAchievement(EmployeeAchievementBase):
    id: int
    awarded_at: datetime
    is_rewarded: bool = False

    class Config:
        from_attributes = True

class LeaderboardEntry(BaseModel):
    rank: int
    employee_name: str
    total_points: int
    level: int
