from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.core.database import get_db
from src.schemas.manufacturing_order import ManufacturingOrder, ManufacturingOrderCreate, ManufacturingOrderUpdate
from src.crud.manufacturing_order import (
    get_manufacturing_order, get_manufacturing_order_by_number, get_manufacturing_orders,
    create_manufacturing_order, update_manufacturing_order, delete_manufacturing_order
)

router = APIRouter(prefix="/manufacturing-orders", tags=["manufacturing-orders"])

@router.get("/", response_model=List[ManufacturingOrder])
def read_manufacturing_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    orders = get_manufacturing_orders(db, skip=skip, limit=limit, status=status)
    return orders

@router.get("/{order_id}", response_model=ManufacturingOrder)
def read_manufacturing_order(order_id: int, db: Session = Depends(get_db)):
    db_order = get_manufacturing_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Manufacturing order not found")
    return db_order

@router.get("/number/{order_number}", response_model=ManufacturingOrder)
def read_manufacturing_order_by_number(order_number: str, db: Session = Depends(get_db)):
    db_order = get_manufacturing_order_by_number(db, order_number=order_number)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Manufacturing order not found")
    return db_order

@router.post("/", response_model=ManufacturingOrder, status_code=status.HTTP_201_CREATED)
def create_new_manufacturing_order(order: ManufacturingOrderCreate, db: Session = Depends(get_db)):
    db_order = get_manufacturing_order_by_number(db, order_number=order.order_number)
    if db_order:
        raise HTTPException(status_code=400, detail="Order number already registered")
    return create_manufacturing_order(db=db, order=order)

@router.put("/{order_id}", response_model=ManufacturingOrder)
def update_existing_manufacturing_order(order_id: int, order: ManufacturingOrderUpdate, db: Session = Depends(get_db)):
    db_order = update_manufacturing_order(db, order_id=order_id, order=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Manufacturing order not found")
    return db_order

@router.delete("/{order_id}")
def delete_manufacturing_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    db_order = delete_manufacturing_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Manufacturing order not found")
    return {"message": "Manufacturing order deleted successfully"}
