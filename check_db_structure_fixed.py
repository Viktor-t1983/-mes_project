import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def check_tables():
    # Получаем и исправляем URL
    db_url = os.getenv("DATABASE_URL")
    if "asyncpg" in db_url:
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    
    print("🔍 СТРУКТУРА БАЗЫ ДАННЫХ")
    print("=" * 40)
    print(f"Подключение: {db_url}")
    
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Получаем список таблиц
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print(f"\n📋 Найдено таблиц: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            print(f"\n📊 Таблица: {table_name}")
            
            # Получаем структуру таблицы
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            
            for col in columns:
                print(f"   📝 {col[0]} ({col[1]}) - nullable: {col[2]}")
        
        cursor.close()
        conn.close()
        print("\n✅ Проверка завершена")
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    check_tables()
