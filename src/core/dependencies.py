from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.employee import Employee

def get_current_employee(db: Session = Depends(get_db)):
    """
    Заглушка для получения текущего сотрудника.
    В реальном приложении здесь будет JWT токен и проверка прав.
    """
    # Временно возвращаем первого сотрудника для тестирования
    employee = db.query(Employee).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return employee
