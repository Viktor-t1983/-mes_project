"""
Срочное исправление импортов в моделях
"""

def fix_employee_import():
    """Исправляем импорт в employee.py"""
    content = '''from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    qr_code = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    role = Column(String)
    allowed_workcenters = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name} - {self.role}>"
'''
    with open("src/models/employee.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Исправлен импорт в employee.py")

def fix_all_imports():
    """Исправляем импорты во всех моделях"""
    models = [
        "operation.py",
        "order.py", 
        "project.py",
        "manufacturing_order.py",
        "defect_report.py"
    ]
    
    for model in models:
        try:
            with open(f"src/models/{model}", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Заменяем импорт
            content = content.replace("from src.database import Base", "from ..database import Base")
            
            with open(f"src/models/{model}", "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Исправлен импорт в {model}")
        except Exception as e:
            print(f"⚠️ Ошибка в {model}: {e}")

if __name__ == "__main__":
    print("🛠 ИСПРАВЛЕНИЕ ИМПОРТОВ В МОДЕЛЯХ")
    fix_employee_import()
    fix_all_imports()
    print("\\n✅ ВСЕ ИМПОРТЫ ИСПРАВЛЕНЫ!")
