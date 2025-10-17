from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from sqlalchemy import select, func, case

router = APIRouter(prefix="/api/v1/analytics", tags=["Day 13 - Analytics"])

@router.get("/oee")
async def get_oee(db: AsyncSession = Depends(get_db)):
    """Overall Equipment Effectiveness по станкам"""
    # Пример упрощённого расчёта
    return {
        "workcenters": [
            {"id": "cnc1", "oee": 87.5, "status": "green"},
            {"id": "laser2", "oee": 62.3, "status": "yellow"},
            {"id": "weld3", "oee": 41.0, "status": "red"}
        ]
    }

@router.get("/projects-status")
async def get_projects_status(db: AsyncSession = Depends(get_db)):
    """Тепловая карта проектов"""
    return {
        "projects": [
            {"id": 4, "name": "Тестовый проект", "status": "green", "days_to_deadline": 5},
            {"id": 5, "name": "Срочный заказ", "status": "red", "days_to_deadline": -2}
        ]
    }
