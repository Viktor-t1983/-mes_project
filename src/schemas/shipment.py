from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShipmentBase(BaseModel):
    project_id: int
    manufacturing_order_id: int
    invoice_number: str
    documents_from_1c: Optional[str] = None

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentConfirm(BaseModel):
    employee_qr: str

class ShipmentTransporterConfirm(BaseModel):
    transporter_qr: str
    tracking_number: str

class Shipment(ShipmentBase):
    id: int
    status: str
    shipped_at: Optional[datetime]
    signature_hash: str

    class Config:
        from_attributes = True
