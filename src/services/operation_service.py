from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.operation import Operation
from src.models.employee import Employee
from src.services.lms_service import LMSService

async def start_operation(db: AsyncSession, operation_id: int, employee_qr: str):
    """Запуск операции с проверкой допуска"""
    # Получаем оператора
    emp = await db.scalar(select(Employee).where(Employee.qr_code == employee_qr))
    if not emp:
        raise ValueError("Сотрудник не найден")

    # Получаем операцию
    op = await db.get(Operation, operation_id)
    if not op:
        raise ValueError("Операция не найдена")

    # Проверяем допуск
    has_auth = await LMSService.check_authorization(
        db, emp.id, op.workcenter_id, op.operation_type
    )
    if not has_auth:
        raise ValueError("Нет допуска к операции. Требуется подтверждение мастера.")

    # Запускаем операцию
    op.status = "in_progress"
    await db.commit()
    return op
