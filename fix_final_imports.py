import os

# Читаем текущий main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Проверяем какие модели импортированы
import_lines = [
    'from src.models.employee import Employee',
    'from src.models.manufacturing_order import ManufacturingOrder', 
    'from src.models.operation import Operation',
    'from src.models.defect_report import DefectReport',
    'from src.models.order import Order',
    'from src.models.project import Project'
]

# Находим блок импортов и заменяем его
import_block_start = content.find('from src.database import get_db, engine, Base')
if import_block_start != -1:
    # Находим конец блока импортов
    import_block_end = content.find('from pydantic import BaseModel')
    
    # Создаем новый блок импортов
    new_imports = 'from src.database import get_db, engine, Base\\n'
    for imp in import_lines:
        new_imports += imp + '\\n'
    
    # Заменяем блок импортов
    old_imports = content[import_block_start:import_block_end]
    content = content.replace(old_imports, new_imports)

# Записываем обратно
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Все модели импортированы в main.py")
