import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv

load_dotenv()

def test_postgres_connection():
    print("🔍 ТЕСТИРОВАНИЕ ПОДКЛЮЧЕНИЯ К POSTGRESQL")
    print("=" * 50)
    
    # Параметры подключения из .env
    database_url = os.getenv('DATABASE_URL')
    print(f"Database URL: {database_url}")
    
    # Парсим параметры из URL
    if database_url:
        # Формат: postgresql+asyncpg://user:password@host:port/database
        try:
            parts = database_url.replace('postgresql+asyncpg://', '').split('@')
            user_pass = parts[0].split(':')
            host_db = parts[1].split('/')
            host_port = host_db[0].split(':')
            
            user = user_pass[0]
            password = user_pass[1] if len(user_pass) > 1 else ''
            host = host_port[0]
            port = host_port[1] if len(host_port) > 1 else '5432'
            database = host_db[1]
            
            print(f"Параметры подключения:")
            print(f"  Хост: {host}")
            print(f"  Порт: {port}")
            print(f"  Пользователь: {user}")
            print(f"  База данных: {database}")
            print(f"  Пароль: {'*' * len(password)}")
            
        except Exception as e:
            print(f"❌ Ошибка парсинга URL: {e}")
            return
    
    # Тестируем подключение
    try:
        print("\n🔄 Попытка подключения к PostgreSQL...")
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="MesProject2025",  # Ваш пароль из .env
            database="postgres"  # Сначала к системной БД
        )
        
        print("✅ Успешное подключение к PostgreSQL!")
        
        # Проверяем существование нашей базы данных
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'mes_db'")
        db_exists = cursor.fetchone()
        
        if db_exists:
            print("✅ База данных 'mes_db' существует")
        else:
            print("❌ База данных 'mes_db' не существует")
            print("Создаем базу данных...")
            cursor.execute("CREATE DATABASE mes_db")
            conn.commit()
            print("✅ База данных 'mes_db' создана")
        
        cursor.close()
        conn.close()
        
        # Тестируем подключение к нашей базе
        print("\n🔄 Подключение к базе 'mes_db'...")
        conn = psycopg2.connect(
            host="localhost",
            port="5432", 
            user="postgres",
            password="MesProject2025",
            database="mes_db"
        )
        print("✅ Успешное подключение к базе 'mes_db'!")
        conn.close()
        
        return True
        
    except OperationalError as e:
        print(f"❌ Ошибка подключения: {e}")
        print("\n🔧 ВОЗМОЖНЫЕ РЕШЕНИЯ:")
        print("1. Убедитесь что PostgreSQL запущен")
        print("2. Проверьте пароль в pgAdmin -> Servers -> PostgreSQL -> Properties")
        print("3. Запустите pgAdmin и проверьте подключение")
        return False

if __name__ == "__main__":
    test_postgres_connection()
