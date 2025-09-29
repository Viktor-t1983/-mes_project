from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.schemas.incentive import Incentive, IncentiveCreate, IncentiveUpdate
from src.crud.incentive import (
    get_incentive, get_incentives_by_employee, get_incentives_by_period,
    create_incentive, update_incentive, mark_incentive_paid
)

router = APIRouter(prefix="/incentives", tags=["incentives"])

@router.get("/", response_model=List[Incentive])
def read_incentives(
    skip: int = 0,
    limit: int = 100,
    employee_id: int = None,
    period: str = None,
    db: Session = Depends(get_db)
):
    if employee_id:
        incentives = get_incentives_by_employee(db, employee_id=employee_id, skip=skip, limit=limit)
    elif period:
        incentives = get_incentives_by_period(db, period=period, skip=skip, limit=limit)
    else:
        incentives = get_incentives_by_employee(db, employee_id=0, skip=skip, limit=limit)  # Empty result
    return incentives

@router.get("/{incentive_id}", response_model=Incentive)
def read_incentive(incentive_id: int, db: Session = Depends(get_db)):
    db_incentive = get_incentive(db, incentive_id=incentive_id)
    if db_incentive is None:
        raise HTTPException(status_code=404, detail="Incentive not found")
    return db_incentive

@router.post("/", response_model=Incentive, status_code=status.HTTP_201_CREATED)
def create_new_incentive(incentive: IncentiveCreate, db: Session = Depends(get_db)):
    return create_incentive(db=db, incentive=incentive)

@router.put("/{incentive_id}", response_model=Incentive)
def update_existing_incentive(incentive_id: int, incentive: IncentiveUpdate, db: Session = Depends(get_db)):
    db_incentive = update_incentive(db, incentive_id=incentive_id, incentive=incentive)
    if db_incentive is None:
        raise HTTPException(status_code=404, detail="Incentive not found")
    return db_incentive

@router.post("/{incentive_id}/mark-paid", response_model=Incentive)
def mark_incentive_paid_endpoint(incentive_id: int, db: Session = Depends(get_db)):
    db_incentive = mark_incentive_paid(db, incentive_id=incentive_id)
    if db_incentive is None:
        raise HTTPException(status_code=404, detail="Incentive not found")
    return db_incentive
