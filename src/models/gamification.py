from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Achievement(Base):
    """Модель достижений для геймификации"""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    points = Column(Integer, default=0)
    badge_icon = Column(String(50), default="🏆")
    is_active = Column(Boolean, default=True)

class EmployeeAchievement(Base):
    """Связь сотрудников с достижениями"""
    __tablename__ = "employee_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    awarded_at = Column(DateTime(timezone=True), server_default=func.now())
    is_rewarded = Column(Boolean, default=False)
    
    employee = relationship("Employee", backref="achievements")
    achievement = relationship("Achievement")

class Leaderboard(Base):
    """Таблица лидеров для геймификации"""
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    employee = relationship("Employee")
