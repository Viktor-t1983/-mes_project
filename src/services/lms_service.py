import hashlib
import hmac
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.lms import Certificate, TrainingCourse, EmployeeTraining, WorkcenterAuthorization
from src.core.config import settings

class LMSService:
    """Сервис управления обучением и допусками"""

    @staticmethod
    def _generate_signature(employee_id: int, course_id: int, issued_at: datetime) -> str:
        """Генерация цифровой подписи сертификата"""
        message = f"{employee_id}:{course_id}:{issued_at.isoformat()}"
        signature = hmac.new(
            settings.SECRET_KEY.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature

    @classmethod
    async def issue_certificate(cls, db: AsyncSession, employee_id: int, course_id: int) -> Certificate:
        """Выдача сертификата после прохождения курса"""
        course = await db.get(TrainingCourse, course_id)
        if not course:
            raise ValueError("Курс не найден")

        issued_at = datetime.utcnow()
        signature = cls._generate_signature(employee_id, course_id, issued_at)

        certificate = Certificate(
            employee_id=employee_id,
            course_id=course_id,
            issued_at=issued_at,
            signature=signature
        )
        db.add(certificate)
        await db.flush()

        # Создаём запись о прохождении
        training = EmployeeTraining(
            employee_id=employee_id,
            course_id=course_id,
            certificate_id=certificate.id
        )
        db.add(training)

        # Выдаём допуск
        auth = WorkcenterAuthorization(
            employee_id=employee_id,
            workcenter_id=course.workcenter_id,
            operation_type=course.operation_type,
            authorized_until=issued_at + timedelta(days=365)  # На 1 год
        )
        db.add(auth)

        await db.commit()
        return certificate

    @classmethod
    async def check_authorization(cls, db: AsyncSession, employee_id: int, workcenter_id: str, operation_type: str) -> bool:
        """Проверка наличия допуска"""
        auth = await db.execute(
            select(WorkcenterAuthorization)
            .where(
                WorkcenterAuthorization.employee_id == employee_id,
                WorkcenterAuthorization.workcenter_id == workcenter_id,
                WorkcenterAuthorization.operation_type == operation_type,
                WorkcenterAuthorization.is_active == True,
                (WorkcenterAuthorization.authorized_until.is_(None) |
                 (WorkcenterAuthorization.authorized_until > datetime.utcnow()))
            )
        )
        return auth.scalar_one_or_none() is not None

    @classmethod
    async def override_authorization(cls, db: AsyncSession, employee_id: int, workcenter_id: str, operation_type: str, master_qr_code: str, reason: str) -> bool:
        """Ручное подтверждение допуска мастером"""
        # Проверяем, что мастер существует и имеет роль 'foreman'
        from src.models.employee import Employee
        master = await db.execute(
            select(Employee).where(Employee.qr_code == master_qr_code, Employee.role == "foreman")
        )
        if not master.scalar_one_or_none():
            return False

        # Создаём запись в аудите
        from src.models.audit_log import AuditLog
        audit = AuditLog(
            user_id=master.scalar().id,
            action="override_authorization",
            data_snapshot=f'{{"employee_id": {employee_id}, "workcenter_id": "{workcenter_id}", "operation_type": "{operation_type}", "reason": "{reason}"}}'
        )
        db.add(audit)
        await db.commit()
        return True
