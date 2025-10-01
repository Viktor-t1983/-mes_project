import subprocess
import os
import psycopg2
from psycopg2 import OperationalError

def check_postgresql():
    print("🔍 ПРОВЕРКА POSTGRESQL")
    print("=" * 40)
    
    # Проверяем доступность PostgreSQL
    try:
        # Пытаемся подключиться к PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            port="5432", 
            user="postgres",
            password="password"  # стандартный пароль, возможно другой
        )
        print("✅ PostgreSQL доступен")
        conn.close()
        return True
    except OperationalError as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        print("\n🔧 ВОЗМОЖНЫЕ ПРИЧИНЫ:")
        print("1. PostgreSQL не запущен")
        print("2. Неправильный пароль")
        print("3. Порт не 5432")
        print("4. Пользователь postgres не существует")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

def check_current_env():
    print("\n📁 ПРОВЕРКА ТЕКУЩИХ НАСТРОЕК .env")
    print("=" * 40)
    
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
            print("Содержимое .env:")
            print(content)
    else:
        print("❌ Файл .env не найден")

if __name__ == "__main__":
    check_current_env()
    print()
    check_postgresql()
