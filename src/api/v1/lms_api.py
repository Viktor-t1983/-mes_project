from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.services.lms_service import LMSService
from src.schemas.lms import TrainingCourseCreate, TrainingCourse, Certificate, AuthorizationOverride

router = APIRouter(prefix="/api/v1/lms", tags=["LMS"])

@router.post("/courses", response_model=TrainingCourse, status_code=status.HTTP_201_CREATED)
async def create_course(course: TrainingCourseCreate, db: AsyncSession = Depends(get_db)):
    """Создание курса обучения"""
    db_course = TrainingCourse(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

@router.post("/complete", response_model=Certificate)
async def complete_course(employee_id: int, course_id: int, db: AsyncSession = Depends(get_db)):
    """Завершение курса и выдача сертификата"""
    try:
        cert = await LMSService.issue_certificate(db, employee_id, course_id)
        return cert
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/authorize")
async def check_authorization(
    employee_id: int,
    workcenter_id: str,
    operation_type: str,
    db: AsyncSession = Depends(get_db)
):
    """Проверка допуска"""
    has_auth = await LMSService.check_authorization(db, employee_id, workcenter_id, operation_type)
    return {"authorized": has_auth}

@router.post("/override", status_code=status.HTTP_202_ACCEPTED)
async def override_authorization(
    override: AuthorizationOverride,
    employee_id: int,
    workcenter_id: str,
    operation_type: str,
    db: AsyncSession = Depends(get_db)
):
    """Подтверждение допуска мастером"""
    success = await LMSService.override_authorization(
        db, employee_id, workcenter_id, operation_type,
        override.master_qr_code, override.reason
    )
    if not success:
        raise HTTPException(status_code=403, detail="Мастер не найден или не имеет прав")
    return {"status": "approved", "message": "Допуск временно разрешён"}
