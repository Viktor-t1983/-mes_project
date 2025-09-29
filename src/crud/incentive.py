from sqlalchemy.orm import Session
from sqlalchemy import and_
from decimal import Decimal
from src.models.incentive import Incentive
from src.schemas.incentive import IncentiveCreate, IncentiveUpdate

def get_incentive(db: Session, incentive_id: int):
    return db.query(Incentive).filter(Incentive.id == incentive_id).first()

def get_incentives_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100):
    return db.query(Incentive).filter(
        Incentive.employee_id == employee_id
    ).offset(skip).limit(limit).all()

def get_incentives_by_period(db: Session, period: str, skip: int = 0, limit: int = 100):
    return db.query(Incentive).filter(
        Incentive.period == period
    ).offset(skip).limit(limit).all()

def create_incentive(db: Session, incentive: IncentiveCreate):
    # Рассчитываем премию на основе показателей
    base_amount = Decimal('1000.00')  # Базовая ставка
    quality_bonus = incentive.quality_score * Decimal('10.00')  # 10 руб за каждый балл качества
    efficiency_bonus = incentive.efficiency_score * Decimal('8.00')  # 8 руб за каждый балл эффективности
    defect_penalty = incentive.defect_count * Decimal('50.00')  # Штраф 50 руб за каждый дефект
    
    total_amount = base_amount + quality_bonus + efficiency_bonus - defect_penalty
    
    db_incentive = Incentive(
        employee_id=incentive.employee_id,
        period=incentive.period,
        completed_operations=incentive.completed_operations,
        quality_score=incentive.quality_score,
        efficiency_score=incentive.efficiency_score,
        defect_count=incentive.defect_count,
        overtime_hours=incentive.overtime_hours,
        base_amount=base_amount,
        quality_bonus=quality_bonus,
        efficiency_bonus=efficiency_bonus,
        defect_penalty=defect_penalty,
        total_amount=total_amount
    )
    db.add(db_incentive)
    db.commit()
    db.refresh(db_incentive)
    return db_incentive

def update_incentive(db: Session, incentive_id: int, incentive: IncentiveUpdate):
    db_incentive = db.query(Incentive).filter(Incentive.id == incentive_id).first()
    if db_incentive:
        update_data = incentive.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_incentive, field, value)
        db.commit()
        db.refresh(db_incentive)
    return db_incentive

def mark_incentive_paid(db: Session, incentive_id: int):
    db_incentive = db.query(Incentive).filter(Incentive.id == incentive_id).first()
    if db_incentive:
        db_incentive.status = "paid"
        from datetime import datetime
        db_incentive.paid_at = datetime.now()
        db.commit()
        db.refresh(db_incentive)
    return db_incentive
