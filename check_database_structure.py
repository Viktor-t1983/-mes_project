import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def check_tables():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    print("🔍 СТРУКТУРА БАЗЫ ДАННЫХ")
    print("=" * 40)
    
    # Получаем список таблиц
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    
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

if __name__ == "__main__":
    check_tables()
