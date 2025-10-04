from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OneCInvoiceBase(BaseModel):
    external_id: str
    invoice_number: str
    amount: int  # в копейках
    currency: str = "RUB"

class OneCInvoiceCreate(OneCInvoiceBase):
    pass

class OneCInvoice(OneCInvoiceBase):
    id: int
    issued_at: Optional[datetime] = None
    synced_at: Optional[datetime] = None
    is_synced: bool = False
    sync_error: Optional[str] = None

    class Config:
        from_attributes = True
