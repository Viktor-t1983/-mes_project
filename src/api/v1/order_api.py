from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models.order import Order as OrderModel
from src.schemas.order import OrderCreate, OrderResponse
from sqlalchemy import select

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    db_order = OrderModel(**order.dict())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order
