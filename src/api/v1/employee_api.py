from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.database import get_db
from src.models.employee import Employee as EmployeeModel
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1/employees", tags=["Employees"])

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    role: str
    qr_code: str

class EmployeeCreate(EmployeeBase):
    pass

@router.post("/", response_model=EmployeeBase, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    db_employee = EmployeeModel(**employee.model_dump())
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee

@router.get("/")
async def list_employees(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmployeeModel))
    return result.scalars().all()
