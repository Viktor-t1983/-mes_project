from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.employee import Employee
from src.schemas.employee import EmployeeCreate, EmployeeUpdate
import random
import string

def generate_employee_qr(length=6):
    """Генерация уникального QR-кода для сотрудника"""
    chars = string.ascii_uppercase + string.digits
    return 'EMP_' + ''.join(random.choice(chars) for _ in range(length))

async def create_employee(db: AsyncSession, employee: EmployeeCreate):
    # Генерируем QR-код если не предоставлен
    qr_code = employee.qr_code or generate_employee_qr()
    
    db_employee = Employee(
        qr_code=qr_code,
        name=employee.name,
        role=employee.role,
        department=employee.department
    )
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee

async def get_employee(db: AsyncSession, employee_id: int):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    return result.scalar_one_or_none()

async def get_employee_by_qr(db: AsyncSession, qr_code: str):
    result = await db.execute(select(Employee).where(Employee.qr_code == qr_code))
    return result.scalar_one_or_none()

async def update_employee(db: AsyncSession, employee_id: int, employee_update: EmployeeUpdate):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    db_employee = result.scalar_one_or_none()
    if db_employee:
        update_data = employee_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_employee, field, value)
        await db.commit()
        await db.refresh(db_employee)
    return db_employee
