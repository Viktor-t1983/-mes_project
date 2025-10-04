from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.core.auth import require_role
from src.core.logger import logger

router = APIRouter(prefix="/mobile", tags=["Mobile API"])

@router.post("/scan-start")
async def mobile_start(
    qr_code: str,
    employee_qr: str,
    current_employee = Depends(require_role("operator")),  # Любой оператор (мобильный или с компа)
    db: Session = Depends(get_db)
):
    """Начало операции — может вызываться с мобильного или с компа"""
    logger.info(
        "Operation start called",
        employee_id=current_employee.id,
        qr_code=qr_code,
        employee_qr=employee_qr,
        source="mobile_or_network"  # Универсальный источник
    )
    return {"status": "started", "operation_id": 123}

@router.get("/my-tasks/{employee_id}")
async def get_employee_tasks(
    employee_id: int,
    current_employee = Depends(require_role("operator")),  # Любой оператор
    db: Session = Depends(get_db)
):
    """Получение сменного задания — может вызываться с мобильного или с компа"""
    logger.info("Get employee tasks called", employee_id=employee_id, source="mobile_or_network")
    return [{"id": 1, "part": "Вал-123", "operation": "Токарная"}]
