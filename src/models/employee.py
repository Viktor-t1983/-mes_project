from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from src.models.base import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    qr_code = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    role = Column(String)
    allowed_workcenters = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name} - {self.role}>"
