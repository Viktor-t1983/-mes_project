from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from .base import Base

class OneCInvoice(Base):
    __tablename__ = "one_c_invoices"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(100), unique=True, nullable=False)
    invoice_number = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)  # в копейках
    currency = Column(String(3), default="RUB")
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    synced_at = Column(DateTime(timezone=True), nullable=True)
    is_synced = Column(Boolean, default=False)
    sync_error = Column(String, nullable=True)
