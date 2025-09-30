from src.core.database import engine
import sqlalchemy as sa

def migrate_employee_table():
    with engine.begin() as conn:
        print('🔄 Начинаем миграцию таблицы employees...')
        
        # 1. Проверяем текущую структуру
        result = conn.execute(sa.text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'employees'
        """))
        
        current_columns = [row[0] for row in result]
        print(f'📋 Текущие колонки: {current_columns}')
        
        # 2. Переименовываем position → role (если position существует)
        if 'position' in current_columns and 'role' not in current_columns:
            conn.execute(sa.text('ALTER TABLE employees RENAME COLUMN position TO role'))
            print('✅ Переименовано position → role')
        
        # 3. Добавляем allowed_workcenters (если нет)
        if 'allowed_workcenters' not in current_columns:
            conn.execute(sa.text('ALTER TABLE employees ADD COLUMN allowed_workcenters TEXT'))
            print('✅ Добавлено allowed_workcenters')
        
        # 4. Удаляем старые поля (если они есть и не нужны)
        if 'department' in current_columns:
            conn.execute(sa.text('ALTER TABLE employees DROP COLUMN department'))
            print('✅ Удален department')
            
        if 'qualifications' in current_columns:
            conn.execute(sa.text('ALTER TABLE employees DROP COLUMN qualifications'))
            print('✅ Удален qualifications')
        
        print('🎉 Миграция завершена успешно!')

if __name__ == "__main__":
    migrate_employee_table()
