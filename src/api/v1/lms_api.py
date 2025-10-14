from fastapi import APIRouter, Depends, HTTPException, Query, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from src.core.database import get_db
from src.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/lms", tags=["LMS"])

class OverrideRequest(BaseModel):
    master_qr_code: str
    reason: str

@router.get("/authorize")
async def check_authorization(
    employee_id: int,
    workcenter_id: str,
    operation_type: str,
    db: AsyncSession = Depends(get_db)
):
    """Проверка допуска"""
    from src.services.lms_service import LMSService
    has_auth = await LMSService.check_authorization(db, employee_id, workcenter_id, operation_type)
    return {"authorized": has_auth}

@router.post("/override", status_code=status.HTTP_202_ACCEPTED)
async def override_authorization(
    employee_id: int = Query(...),
    workcenter_id: str = Query(...),
    operation_type: str = Query(...),
    override: OverrideRequest = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """Подтверждение допуска мастером"""
    from src.models.employee import Employee
    operator = await db.get(Employee, employee_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Оператор не найден")

    try:
        _, master = await AuthService.confirm_override(
            db=db,
            operator_qr=operator.qr_code,
            master_qr=override.master_qr_code,
            reason=override.reason,
            context={
                "workcenter_id": workcenter_id,
                "operation_type": operation_type,
                "employee_id": employee_id
            }
        )
    except HTTPException:
        raise

    # Убран вызов LMSService.override_authorization — всё уже в аудите
    return {"status": "approved", "by_master": master.id}
