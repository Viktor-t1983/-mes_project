from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TrainingCourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    operation_type: str
    workcenter_id: str
    duration_hours: Optional[int] = 8

class TrainingCourseCreate(TrainingCourseBase):
    pass

class TrainingCourse(TrainingCourseBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class CertificateBase(BaseModel):
    employee_id: int
    course_id: int
    expires_at: Optional[datetime] = None

class Certificate(CertificateBase):
    id: int
    issued_at: datetime
    signature: str
    is_revoked: bool

    class Config:
        from_attributes = True

class AuthorizationOverride(BaseModel):
    """Подтверждение мастера для исключения"""
    master_qr_code: str
    reason: str
