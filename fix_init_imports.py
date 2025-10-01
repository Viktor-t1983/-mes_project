"""
Убедимся что в __init__.py нет неправильных импортов
"""

# Чистый __init__.py без импорта Base
init_content = '''from .employee import Employee
from .manufacturing_order import ManufacturingOrder
from .operation import Operation
from .defect_report import DefectReport
from .order import Order
from .project import Project
'''

with open("src/models/__init__.py", "w", encoding="utf-8") as f:
    f.write(init_content)

print("✅ src/models/__init__.py очищен от неправильных импортов")
