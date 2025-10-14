import hashlib
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.lms import Certificate, TrainingCourse, EmployeeTraining, WorkcenterAuthorization
from src.models.audit_log import AuditLog
from src.core.config import settings

class LMSService:
    @staticmethod
    def _generate_signature(employee_id: int, course_id: int, issued_at: datetime) -> str:
        payload = f"{employee_id}:{course_id}:{issued_at.isoformat()}:{settings.SECRET_KEY}"
        return hashlib.sha256(payload.encode()).hexdigest()

    @classmethod
    async def issue_certificate(cls, db: AsyncSession, employee_id: int, course_id: int):
        course = await db.get(TrainingCourse, course_id)
        if not course:
            raise ValueError("Курс не найден")
        issued_at = datetime.utcnow()
        signature = cls._generate_signature(employee_id, course_id, issued_at)
        certificate = Certificate(
            employee_id=employee_id,
            course_id=course_id,
            issued_at=issued_at,
            expires_at=issued_at + timedelta(days=365),
            signature=signature,
            is_revoked=False
        )
        db.add(certificate)
        await db.commit()
        return certificate

    @classmethod
    async def check_authorization(cls, db: AsyncSession, employee_id: int, workcenter_id: str, operation_type: str) -> bool:
        auth = await db.execute(
            select(WorkcenterAuthorization).where(
                WorkcenterAuthorization.employee_id == employee_id,
                WorkcenterAuthorization.workcenter_id == workcenter_id,
                WorkcenterAuthorization.operation_type == operation_type,
                WorkcenterAuthorization.is_active == True
            )
        )
        return auth.scalar_one_or_none() is not None

    @classmethod
    async def override_authorization(cls, db: AsyncSession, employee_id: int, workcenter_id: str, operation_type: str, master_qr_code: str, reason: str) -> bool:
        # Создаём запись в аудите напрямую — без повторного запроса к Employee
        audit = AuditLog(
            user_id=None,  # ← Будет установлено в AuthService
            action="lms_override_record",
            data_snapshot=f'{{"employee_id": {employee_id}, "workcenter_id": "{workcenter_id}", "operation_type": "{operation_type}", "reason": "{reason}"}}'
        )
        db.add(audit)
        await db.commit()
        return True
