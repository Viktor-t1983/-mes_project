from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.database import get_db
from src.models.order import Order as OrderModel
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])

class OrderBase(BaseModel):
    name: str
    product_name: str
    quantity: int
    project_id: Optional[int] = None

class OrderCreate(OrderBase):
    pass

@router.post("/", response_model=OrderBase, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    db_order = OrderModel(**order.model_dump())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

@router.get("/")
async def list_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderModel))
    return result.scalars().all()
