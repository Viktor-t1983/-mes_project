from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from src.core.database import get_db
from src.schemas.warehouse_item import WarehouseItem, WarehouseItemCreate, WarehouseItemUpdate
from src.crud.warehouse_item import (
    get_warehouse_item, get_warehouse_item_by_code, get_warehouse_items,
    create_warehouse_item, update_warehouse_item, update_warehouse_quantity, deactivate_warehouse_item
)

router = APIRouter(prefix="/warehouse-items", tags=["warehouse-items"])

@router.get("/", response_model=List[WarehouseItem])
def read_warehouse_items(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = Query(None, description="Filter by category"),
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    items = get_warehouse_items(db, skip=skip, limit=limit, category=category, active_only=active_only)
    return items

@router.get("/{item_id}", response_model=WarehouseItem)
def read_warehouse_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_warehouse_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Warehouse item not found")
    return db_item

@router.get("/code/{item_code}", response_model=WarehouseItem)
def read_warehouse_item_by_code(item_code: str, db: Session = Depends(get_db)):
    db_item = get_warehouse_item_by_code(db, item_code=item_code)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Warehouse item not found")
    return db_item

@router.post("/", response_model=WarehouseItem, status_code=status.HTTP_201_CREATED)
def create_new_warehouse_item(item: WarehouseItemCreate, db: Session = Depends(get_db)):
    db_item = get_warehouse_item_by_code(db, item_code=item.item_code)
    if db_item:
        raise HTTPException(status_code=400, detail="Item code already registered")
    return create_warehouse_item(db=db, item=item)

@router.put("/{item_id}", response_model=WarehouseItem)
def update_existing_warehouse_item(item_id: int, item: WarehouseItemUpdate, db: Session = Depends(get_db)):
    db_item = update_warehouse_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Warehouse item not found")
    return db_item

@router.post("/{item_id}/update-quantity", response_model=WarehouseItem)
def update_warehouse_quantity_endpoint(
    item_id: int, 
    quantity_change: Decimal,
    db: Session = Depends(get_db)
):
    db_item = update_warehouse_quantity(db, item_id=item_id, quantity_change=quantity_change)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Warehouse item not found")
    return db_item

@router.delete("/{item_id}", response_model=WarehouseItem)
def deactivate_warehouse_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    db_item = deactivate_warehouse_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Warehouse item not found")
    return db_item
