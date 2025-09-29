from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from decimal import Decimal

class IncentiveBase(BaseModel):
    period: str  # YYYY-MM
    completed_operations: int = 0
    quality_score: Decimal = Decimal('0')
    efficiency_score: Decimal = Decimal('0')
    defect_count: int = 0
    overtime_hours: Decimal = Decimal('0')

class IncentiveCreate(IncentiveBase):
    employee_id: int

class IncentiveUpdate(BaseModel):
    completed_operations: Optional[int] = None
    quality_score: Optional[Decimal] = None
    efficiency_score: Optional[Decimal] = None
    defect_count: Optional[int] = None
    overtime_hours: Optional[Decimal] = None
    base_amount: Optional[Decimal] = None
    quality_bonus: Optional[Decimal] = None
    efficiency_bonus: Optional[Decimal] = None
    defect_penalty: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    status: Optional[str] = None
    paid_at: Optional[datetime] = None
    notes: Optional[str] = None

class Incentive(IncentiveBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    employee_id: int
    calculation_date: datetime
    base_amount: Decimal = Decimal('0')
    quality_bonus: Decimal = Decimal('0')
    efficiency_bonus: Decimal = Decimal('0')
    defect_penalty: Decimal = Decimal('0')
    total_amount: Decimal = Decimal('0')
    status: str = "calculated"
    paid_at: Optional[datetime] = None
    notes: Optional[str] = None
