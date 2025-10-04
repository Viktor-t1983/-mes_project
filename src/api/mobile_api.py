from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/mobile", tags=["Mobile API"])

@router.post("/scan-start")
async def mobile_start(qr_code: str, employee_qr: str, db: Session = Depends(get_db)):
    """Начало операции через мобильное приложение"""
    return {"status": "started", "operation_id": 123}

@router.get("/my-tasks/{employee_id}")
async def get_employee_tasks(employee_id: int, db: Session = Depends(get_db)):
    """Получение сменного задания"""
    return [{"id": 1, "part": "Вал-123", "operation": "Токарная"}]
