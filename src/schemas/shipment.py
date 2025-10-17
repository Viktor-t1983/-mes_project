from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import hashlib

class ShipmentBase(BaseModel):
    project_id: int
    manufacturing_order_id: int
    invoice_number: str

class ShipmentCreate(ShipmentBase):
    pass  # signature_hash генерируется автоматически

class ShipmentConfirm(BaseModel):
    employee_qr: str

class ShipmentTransporterConfirm(BaseModel):
    transporter_qr: str
    tracking_number: str

class ShipmentResponse(ShipmentBase):
    id: int
    status: str
    shipped_at: Optional[datetime]
    signature_hash: str

    class Config:
        from_attributes = True
