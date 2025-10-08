from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.models.base import Base

class TrainingCourse(Base):
    """Курс обучения"""
    __tablename__ = "training_courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    operation_type = Column(String, nullable=False)
    workcenter_id = Column(String, nullable=False)  # ← Строка, а не число
    duration_hours = Column(Integer, default=8)
    is_active = Column(Boolean, default=True)

class EmployeeTraining(Base):
    """Прохождение курса сотрудником"""
    __tablename__ = "employee_trainings"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("training_courses.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    certificate_id = Column(Integer, ForeignKey("certificates.id"), nullable=True)

class Certificate(Base):
    """Электронный сертификат"""
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("training_courses.id"), nullable=False)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    signature = Column(String, nullable=False)
    is_revoked = Column(Boolean, default=False)

class WorkcenterAuthorization(Base):
    """Допуск к участку/станку"""
    __tablename__ = "workcenter_authorizations"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    workcenter_id = Column(String, nullable=False)  # ← Ключевое исправление: String
    operation_type = Column(String, nullable=False)
    authorized_until = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
