from functools import wraps
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from typing import List, Optional

# Простая заглушка для require_role (без реальной аутентификации)
def require_role(allowed_roles: List[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # В production: проверка токена, роли из JWT и т.д.
            # Сейчас: пропускаем всех (для тестов)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Альтернатива: если используется Depends
from fastapi import Depends

async def get_current_user_role() -> str:
    # Заглушка: возвращает роль по умолчанию
    return "operator"

def RoleChecker(allowed_roles: List[str]):
    async def check_role(role: str = Depends(get_current_user_role)):
        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Недостаточно прав")
        return role
    return check_role
