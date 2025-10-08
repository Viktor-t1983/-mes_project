from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models.employee import Employee
from sqlalchemy import select

router = APIRouter(tags=["Mobile"])

class ScanStartRequest(BaseModel):
    qr_code: str
    part_number: str

@router.post("/scan-start")
async def scan_start(
    request: ScanStartRequest,
    db: AsyncSession = Depends(get_db)
):
    emp = await db.scalar(select(Employee).where(Employee.qr_code == request.qr_code))
    if not emp:
        raise HTTPException(status_code=404, detail="Оператор не найден")

    from src.services.lms_service import LMSService
    has_auth = await LMSService.check_authorization(db, emp.id, "WC-DEFAULT", "default_op")

    if not has_auth:
        return {
            "status": "requires_approval",
            "message": "Требуется подтверждение мастера",
            "operator_id": emp.id
        }

    return {
        "status": "ok",
        "operator": f"{emp.first_name} {emp.last_name}",
        "part_number": request.part_number
    }
