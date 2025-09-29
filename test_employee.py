from src.core.database import SessionLocal
from src.models.employee import Employee

# Проверим структуру таблицы сотрудников
db = SessionLocal()
try:
    employees_count = db.query(Employee).count()
    print(f"📊 Сотрудников в базе: {employees_count}")
    
    # Проверим структуру таблицы
    from sqlalchemy import inspect
    inspector = inspect(db.bind)
    columns = inspector.get_columns('employees')
    print("📋 Столбцы таблицы employees:")
    for col in columns:
        print(f"   {col['name']} ({col['type']}) - nullable: {col['nullable']}")
        
finally:
    db.close()
