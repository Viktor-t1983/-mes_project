from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.core.database import get_db
from src.models.order import Order
from src.models.project import Project
from src.schemas.order import OrderCreate, Order, OrderUpdate, OrderWithProject

router = APIRouter()

@router.get("/orders", response_model=list[Order], summary="Получить все заказы")
async def get_orders(db: AsyncSession = Depends(get_db)):
    """
    Получить список всех заказов.
    """
    result = await db.execute(select(Order))
    return result.scalars().all()

@router.get("/orders/{order_id}", response_model=OrderWithProject, summary="Получить заказ по ID")
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить заказ по его идентификатору с информацией о проекте.
    """
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заказ с ID {order_id} не найден"
        )
    return order

@router.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED, summary="Создать новый заказ")
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать новый заказ.
    """
    # Проверяем что проект существует
    result = await db.execute(select(Project).where(Project.id == order.project_id))
    if result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проект с ID {order.project_id} не найден"
        )
    
    db_order = Order(**order.dict())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

@router.get("/projects/{project_id}/orders", response_model=list[Order], summary="Получить заказы проекта")
async def get_project_orders(project_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить все заказы конкретного проекта.
    """
    result = await db.execute(select(Order).where(Order.project_id == project_id))
    return result.scalars().all()
