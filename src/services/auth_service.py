"""
AuthService — ядро безопасности MES-системы.
Реализует проверку идентичности, роли и контекстных разрешений.
Senior Security Engineer Edition.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.employee import Employee
from src.models.audit_log import AuditLog
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Единая точка входа для всех проверок безопасности."""

    @staticmethod
    async def authenticate_by_qr(db: AsyncSession, qr_code: str) -> Employee:
        """Аутентифицирует сотрудника по QR-коду. Не проверяет роль."""
        employee = await db.scalar(select(Employee).where(Employee.qr_code == qr_code))
        if not employee:
            logger.warning(f"Неизвестный QR-код: {qr_code}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный QR-код"
            )
        logger.info(f"Аутентификация успешна: {employee.role} {employee.first_name} (ID={employee.id})")
        return employee  # ← Возвращает объект без проверки роли

    @staticmethod
    async def require_role(db: AsyncSession, qr_code: str, required_role: str) -> Employee:
        """Требует сотрудника с указанной ролью."""
        emp = await AuthService.authenticate_by_qr(db, qr_code)
        if emp.role != required_role:
            logger.warning(f"Отказано в доступе: {emp.role} != {required_role}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Требуется роль: {required_role}"
            )
        return emp

    @staticmethod
    async def log_action(db: AsyncSession, action: str, user_id: int,  dict):
        """Логирует безопасное действие в audit_log."""
        log_entry = AuditLog(
            action=action,
            user_id=user_id,
            data_snapshot=str(data)
        )
        db.add(log_entry)
        await db.commit()
        logger.info(f"Audit: {action} by {user_id}")

    @staticmethod
    async def confirm_override(
        db: AsyncSession,
        operator_qr: str,
        master_qr: str,
        reason: str,
        context: dict
    ) -> tuple[Employee, Employee]:
        operator = await AuthService.authenticate_by_qr(db, operator_qr)
        master = await AuthService.require_role(db, master_qr, "foreman")

        await AuthService.log_action(db, "override_authorization", master.id, {
            "operator_id": operator.id,
            "reason": reason,
            **context
        })

        return operator, master
