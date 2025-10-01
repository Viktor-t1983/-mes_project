import os

# Читаем текущий main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим место где импортируются модели и добавляем все модели
import_lines = '''from src.database import get_db, engine, Base
from src.models.employee import Employee
from src.models.manufacturing_order import ManufacturingOrder
from src.models.operation import Operation
from src.models.defect_report import DefectReport
from src.models.order import Order
from src.models.project import Project'''

# Заменяем импорты
old_imports = '''from src.database import get_db, engine, Base
from src.models.employee import Employee
from src.models.manufacturing_order import ManufacturingOrder
from src.models.operation import Operation
from src.models.defect_report import DefectReport
from src.models.order import Order
from src.models.project import Project'''

if old_imports in content:
    content = content.replace(old_imports, import_lines)

# Добавляем CORS middleware после создания app
cors_code = '''from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)'''

# Вставляем CORS после создания app
if 'app = FastAPI(title="MES System"' in content and 'CORSMiddleware' not in content:
    app_line = 'app = FastAPI(title="MES System", version="1.0.0")'
    replacement = app_line + '\\n\\n' + cors_code
    content = content.replace(app_line, replacement)

# Записываем обратно
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Main.py исправлен - добавлены все модели и CORS")
