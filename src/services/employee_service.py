import secrets
import string
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.employee import Employee

def generate_employee_qr(length=8):
    chars = string.ascii_uppercase + string.digits
    return 'EMP_' + ''.join(secrets.choice(chars) for _ in range(length))

# ... остальной код ...
