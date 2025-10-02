from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.models.manufacturing_order import ManufacturingOrder
from src.schemas.manufacturing_order import ManufacturingOrderCreate, ManufacturingOrderCreate

def get_manufacturing_order(db: Session, order_id: int):
    return db.query(ManufacturingOrder).filter(ManufacturingOrder.id == order_id).first()

def get_manufacturing_order_by_number(db: Session, order_number: str):
    return db.query(ManufacturingOrder).filter(ManufacturingOrder.order_number == order_number).first()

def get_manufacturing_orders(db: Session, skip: int = 0, limit: int = 100, status: str = None):
    query = db.query(ManufacturingOrder)
    if status:
        query = query.filter(ManufacturingOrder.status == status)
    return query.offset(skip).limit(limit).all()

def create_manufacturing_order(db: Session, order: ManufacturingOrderCreate):
    db_order = ManufacturingOrder(
        order_number=order.order_number,
        customer_order_id=order.customer_order_id,
        product_name=order.product_name,
        product_code=order.product_code,
        quantity=order.quantity,
        planned_start=order.planned_start,
        planned_end=order.planned_end,
        status=order.status,
        priority=order.priority,
        notes=order.notes
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_manufacturing_order(db: Session, order_id: int, order: ManufacturingOrderCreate):
    db_order = db.query(ManufacturingOrder).filter(ManufacturingOrder.id == order_id).first()
    if db_order:
        update_data = order.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_manufacturing_order(db: Session, order_id: int):
    db_order = db.query(ManufacturingOrder).filter(ManufacturingOrder.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order
