from fastapi import FastAPI
import sys
import os

# Добавляем src в путь для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Импорты ядра
from src.core.logger import logger
from src.core.security import setup_security_middleware

# Импорт моделей для Alembic
from src.models.base import Base
from src.models.order import Order
from src.models.employee import Employee
from src.models.manufacturing_order import ManufacturingOrder
from src.models.operation import Operation
from src.models.defect_report import DefectReport
from src.models.machine import Machine
from src.models.project import Project
from src.models.meta_process import MetaProcess, MetaStep
from src.models.lms import TrainingCourse, EmployeeTraining, Certificate, WorkcenterAuthorization
from src.models.audit_log import AuditLog

app = FastAPI(
    title='MES System - Day 8',
    description='Manufacturing Execution System with LMS and Authorization',
    version='1.0.0'
)

# Подключаем security middleware
setup_security_middleware(app)

# Роутеры
try:
    from src.api.health import router as health_router
    app.include_router(health_router)
    print('✅ Health router connected')
except ImportError as e:
    print(f'❌ Health router error: {e}')

try:
    from src.api.day4_endpoints import router as day4_router
    app.include_router(day4_router)
    print('✅ Day4 router connected')
except ImportError as e:
    print(f'❌ Day4 router error: {e}')

try:
    from src.api.mobile_api import router as mobile_router
    app.include_router(mobile_router, prefix="/mobile")
    print('[OK] Mobile router connected')
except ImportError as e:
    print(f'[ERROR] Mobile router error: {e}')

try:
    from src.api.v1.iiot import router as iiot_router
    app.include_router(iiot_router)
    print("[OK] IIoT router connected")
except Exception as e:
    print(f"[ERROR] IIoT router: {e}")

try:
    from src.api.v1.audit import router as audit_router
    app.include_router(audit_router)
    print("[OK] Audit router connected")
except Exception as e:
    print(f"[ERROR] Audit router: {e}")

try:
    from src.api.v1.meta_api import router as meta_router
    app.include_router(meta_router)
    print("[OK] Meta BPM router connected")
except Exception as e:
    print(f"[ERROR] Meta BPM: {e}")

try:
    from src.api.v1.project_api import router as project_router
    app.include_router(project_router)
    print("[OK] Project router connected")
except Exception as e:
    print(f"[ERROR] Project router: {e}")

try:
    from src.api.v1.order_api import router as order_router
    app.include_router(order_router)
    print("[OK] Order router connected")
except Exception as e:
    print(f"[ERROR] Order router: {e}")

try:
    from src.api.v1.lms_api import router as lms_router
    app.include_router(lms_router)
    print("[OK] LMS router connected")
except Exception as e:
    print(f"[ERROR] LMS router: {e}")

try:
    from src.api.v1.employee_api import router as employee_router
    app.include_router(employee_router)
    print("[OK] Employee router connected")
except Exception as e:
    print(f"[ERROR] Employee router: {e}")

@app.get('/')
async def root():
    return {
        'message': 'MES System API - Day 8 Fully Operational',
        'version': '1.0.0',
        'status': 'running'
    }

if __name__ == '__main__':
    import uvicorn
    print('🚀 Starting MES Day 8 Server on port 8000...')
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)
