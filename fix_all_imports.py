"""
Исправляем все импорты на абсолютные пути
"""

def fix_model_imports():
    models = [
        "employee.py",
        "operation.py", 
        "order.py",
        "project.py",
        "manufacturing_order.py",
        "defect_report.py"
    ]
    
    for model in models:
        filepath = f"src/models/{model}"
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Заменяем относительные импорты на абсолютные
            content = content.replace("from ..database import Base", "from src.database import Base")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Исправлен импорт в {model}")
        except Exception as e:
            print(f"❌ Ошибка в {model}: {e}")

def fix_init_file():
    """Исправляем __init__.py в models"""
    init_content = '''from .employee import Employee
from .manufacturing_order import ManufacturingOrder
from .operation import Operation
from .defect_report import DefectReport
from .order import Order
from .project import Project
'''
    with open("src/models/__init__.py", "w", encoding="utf-8") as f:
        f.write(init_content)
    print("✅ Исправлен src/models/__init__.py")

if __name__ == "__main__":
    print("🛠 ИСПРАВЛЕНИЕ ВСЕХ ИМПОРТОВ")
    fix_model_imports()
    fix_init_file()
    print("\\n✅ ВСЕ ИМПОРТЫ ИСПРАВЛЕНЫ!")
