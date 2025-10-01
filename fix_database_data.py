import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def fix_data():
    db_url = os.getenv("DATABASE_URL")
    if "asyncpg" in db_url:
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    
    print("🛠 ИСПРАВЛЕНИЕ ДАННЫХ В БАЗЕ")
    print("=" * 35)
    
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Исправляем данные в orders
        print("\n📝 Исправляем таблицу orders...")
        cursor.execute("""
            UPDATE orders 
            SET 
                name = COALESCE(name, 'Заказ ' || id::text),
                description = COALESCE(description, 'Описание заказа ' || id::text),
                project_id = COALESCE(project_id, 1)
            WHERE name IS NULL OR description IS NULL
        """)
        print(f"✅ Исправлено записей в orders: {cursor.rowcount}")
        
        # Исправляем данные в operations
        print("📝 Исправляем таблицу operations...")
        cursor.execute("""
            UPDATE operations 
            SET 
                planned_duration = COALESCE(planned_duration, 60.0),
                actual_duration = COALESCE(actual_duration, 0.0),
                operation_type = COALESCE(operation_type, 'production'),
                workcenter_id = COALESCE(workcenter_id, 1)
            WHERE planned_duration IS NULL
        """)
        print(f"✅ Исправлено записей в operations: {cursor.rowcount}")
        
        # Исправляем данные в employees (allowed_workcenters)
        print("📝 Исправляем таблицу employees...")
        cursor.execute("""
            UPDATE employees 
            SET allowed_workcenters = '[]'::jsonb
            WHERE allowed_workcenters IS NULL
        """)
        print(f"✅ Исправлено записей в employees: {cursor.rowcount}")
        
        # Проверяем текущие данные
        print("\n🔍 ПРОВЕРКА ИСПРАВЛЕННЫХ ДАННЫХ:")
        
        cursor.execute("SELECT COUNT(*) FROM orders WHERE name IS NULL OR description IS NULL")
        null_orders = cursor.fetchone()[0]
        print(f"📊 Orders с NULL значениями: {null_orders}")
        
        cursor.execute("SELECT COUNT(*) FROM operations WHERE planned_duration IS NULL")
        null_operations = cursor.fetchone()[0]
        print(f"📊 Operations с NULL planned_duration: {null_operations}")
        
        cursor.execute("SELECT COUNT(*) FROM employees WHERE allowed_workcenters IS NULL")
        null_employees = cursor.fetchone()[0]
        print(f"📊 Employees с NULL allowed_workcenters: {null_employees}")
        
        print("\n🎉 ДАННЫЕ В БАЗЕ ИСПРАВЛЕНЫ!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    fix_data()
