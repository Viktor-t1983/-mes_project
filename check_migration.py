from src.core.database import engine
import sqlalchemy as sa

with engine.connect() as conn:
    result = conn.execute(sa.text('''
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'employees' 
        ORDER BY ordinal_position
    '''))
    
    print('✅ Финальная структура employees:')
    for row in result:
        print(f'  {row[0]}: {row[1]}')

# Проверяем что модель работает
from src.core.database import SessionLocal
from src.models.employee import Employee

db = SessionLocal()
try:
    employees = db.query(Employee).all()
    print(f'✅ Найдено сотрудников: {len(employees)}')
    for emp in employees[:3]:
        print(f'  {emp.first_name} {emp.last_name} - {emp.role}')
finally:
    db.close()
