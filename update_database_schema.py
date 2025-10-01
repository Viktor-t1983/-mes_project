import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def update_schema():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    print("🛠 ОБНОВЛЕНИЕ СТРУКТУРЫ БАЗЫ ДАННЫХ")
    print("=" * 45)
    
    try:
        # Добавляем недостающие столбцы в orders
        print("📝 Обновляем таблицу orders...")
        cursor.execute("""
            ALTER TABLE orders 
            ADD COLUMN IF NOT EXISTS project_id INTEGER DEFAULT 1,
            ADD COLUMN IF NOT EXISTS name VARCHAR,
            ADD COLUMN IF NOT EXISTS description TEXT
        """)
        print("✅ orders обновлена")
        
        # Добавляем недостающие столбцы в operations
        print("📝 Обновляем таблицу operations...")
        cursor.execute("""
            ALTER TABLE operations 
            ADD COLUMN IF NOT EXISTS operation_type VARCHAR DEFAULT 'production',
            ADD COLUMN IF NOT EXISTS workcenter_id INTEGER DEFAULT 1
        """)
        print("✅ operations обновлена")
        
        # Добавляем недостающие столбцы в projects
        print("📝 Обновляем таблицу projects...")
        cursor.execute("""
            ALTER TABLE projects 
            ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'active'
        """)
        print("✅ projects обновлена")
        
        # Обновляем employees.allowed_workcenters
        print("📝 Обновляем таблицу employees...")
        cursor.execute("""
            ALTER TABLE employees 
            ALTER COLUMN allowed_workcenters TYPE JSONB USING 
            CASE 
                WHEN allowed_workcenters IS NULL THEN '[]'::jsonb
                ELSE allowed_workcenters::jsonb
            END
        """)
        print("✅ employees обновлена")
        
        print("\n🎉 СТРУКТУРА БАЗЫ ДАННЫХ ОБНОВЛЕНА!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    update_schema()
