import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def update_schema():
    # Получаем и исправляем URL
    db_url = os.getenv("DATABASE_URL")
    if "asyncpg" in db_url:
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    
    print("🛠 ОБНОВЛЕНИЕ СТРУКТУРЫ БАЗЫ ДАННЫХ")
    print("=" * 45)
    print(f"Подключение: {db_url}")
    
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Добавляем недостающие столбцы в orders
        print("\n📝 Обновляем таблицу orders...")
        try:
            cursor.execute("""
                ALTER TABLE orders 
                ADD COLUMN IF NOT EXISTS project_id INTEGER DEFAULT 1,
                ADD COLUMN IF NOT EXISTS name VARCHAR,
                ADD COLUMN IF NOT EXISTS description TEXT
            """)
            print("✅ orders обновлена")
        except Exception as e:
            print(f"⚠️  Ошибка orders: {e}")
        
        # Добавляем недостающие столбцы в operations
        print("📝 Обновляем таблицу operations...")
        try:
            cursor.execute("""
                ALTER TABLE operations 
                ADD COLUMN IF NOT EXISTS operation_type VARCHAR DEFAULT 'production',
                ADD COLUMN IF NOT EXISTS workcenter_id INTEGER DEFAULT 1
            """)
            print("✅ operations обновлена")
        except Exception as e:
            print(f"⚠️  Ошибка operations: {e}")
        
        # Добавляем недостающие столбцы в projects
        print("📝 Обновляем таблицу projects...")
        try:
            cursor.execute("""
                ALTER TABLE projects 
                ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'active'
            """)
            print("✅ projects обновлена")
        except Exception as e:
            print(f"⚠️  Ошибка projects: {e}")
        
        # Обновляем employees.allowed_workcenters
        print("📝 Обновляем таблицу employees...")
        try:
            # Сначала проверяем тип столбца
            cursor.execute("""
                SELECT data_type 
                FROM information_schema.columns 
                WHERE table_name = 'employees' AND column_name = 'allowed_workcenters'
            """)
            result = cursor.fetchone()
            
            if result and result[0] != 'jsonb':
                cursor.execute("""
                    ALTER TABLE employees 
                    ALTER COLUMN allowed_workcenters TYPE JSONB 
                    USING COALESCE(allowed_workcenters::jsonb, '[]'::jsonb)
                """)
            print("✅ employees обновлена")
        except Exception as e:
            print(f"⚠️  Ошибка employees: {e}")
        
        print("\n🎉 СТРУКТУРА БАЗЫ ДАННЫХ ОБНОВЛЕНА!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    update_schema()
