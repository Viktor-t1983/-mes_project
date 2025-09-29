from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from decimal import Decimal

class WarehouseItemBase(BaseModel):
    item_code: str
    name: str
    description: Optional[str] = None
    category: str
    unit: str
    current_quantity: Decimal = Decimal('0')
    min_quantity: Decimal = Decimal('0')
    max_quantity: Optional[Decimal] = None
    location: Optional[str] = None
    supplier: Optional[str] = None

class WarehouseItemCreate(WarehouseItemBase):
    pass

class WarehouseItemUpdate(BaseModel):
    item_code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    current_quantity: Optional[Decimal] = None
    min_quantity: Optional[Decimal] = None
    max_quantity: Optional[Decimal] = None
    location: Optional[str] = None
    supplier: Optional[str] = None
    is_active: Optional[bool] = None
    last_restocked: Optional[datetime] = None

class WarehouseItem(WarehouseItemBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool = True
    last_restocked: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
