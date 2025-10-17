from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
import hashlib
from datetime import datetime

class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    manufacturing_order_id = Column(Integer, ForeignKey("manufacturing_orders.id"), nullable=False)
    invoice_number = Column(String, nullable=False)
    tracking_number = Column(String, nullable=True)
    status = Column(String, default="created")
    shipped_at = Column(DateTime(timezone=True), nullable=True)
    confirmed_by_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    transporter_qr = Column(String, nullable=True)
    documents_from_1c = Column(Text, nullable=True)
    signature_hash = Column(String(64), nullable=False, unique=True)

    project = relationship("Project", back_populates="shipments")
    manufacturing_order = relationship("ManufacturingOrder", back_populates="shipments")

    @staticmethod
    def generate_signature(project_id, mo_id, invoice_number):
        payload = f"{project_id}:{mo_id}:{invoice_number}:{datetime.utcnow().isoformat()}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()
