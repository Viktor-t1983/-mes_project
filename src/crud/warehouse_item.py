from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.models.warehouse_item import WarehouseItem
from src.schemas.warehouse_item import WarehouseItemCreate, WarehouseItemUpdate

def get_warehouse_item(db: Session, item_id: int):
    return db.query(WarehouseItem).filter(WarehouseItem.id == item_id).first()

def get_warehouse_item_by_code(db: Session, item_code: str):
    return db.query(WarehouseItem).filter(WarehouseItem.item_code == item_code).first()

def get_warehouse_items(db: Session, skip: int = 0, limit: int = 100, category: str = None, active_only: bool = True):
    query = db.query(WarehouseItem)
    if category:
        query = query.filter(WarehouseItem.category == category)
    if active_only:
        query = query.filter(WarehouseItem.is_active == True)
    return query.offset(skip).limit(limit).all()

def create_warehouse_item(db: Session, item: WarehouseItemCreate):
    db_item = WarehouseItem(
        item_code=item.item_code,
        name=item.name,
        description=item.description,
        category=item.category,
        unit=item.unit,
        current_quantity=item.current_quantity,
        min_quantity=item.min_quantity,
        max_quantity=item.max_quantity,
        location=item.location,
        supplier=item.supplier
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_warehouse_item(db: Session, item_id: int, item: WarehouseItemUpdate):
    db_item = db.query(WarehouseItem).filter(WarehouseItem.id == item_id).first()
    if db_item:
        update_data = item.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def update_warehouse_quantity(db: Session, item_id: int, quantity_change: float):
    db_item = db.query(WarehouseItem).filter(WarehouseItem.id == item_id).first()
    if db_item:
        db_item.current_quantity += quantity_change
        from datetime import datetime
        if quantity_change > 0:
            db_item.last_restocked = datetime.now()
        db.commit()
        db.refresh(db_item)
    return db_item

def deactivate_warehouse_item(db: Session, item_id: int):
    db_item = db.query(WarehouseItem).filter(WarehouseItem.id == item_id).first()
    if db_item:
        db_item.is_active = False
        db.commit()
        db.refresh(db_item)
    return db_item
