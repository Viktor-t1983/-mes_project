import os
import subprocess

def check_and_create_migrations():
    print("🗃️ ПРОВЕРКА МИГРАЦИЙ БАЗЫ ДАННЫХ")
    
    migrations_dir = "migrations/versions"
    
    # Проверяем есть ли файлы миграций
    if os.path.exists(migrations_dir) and os.listdir(migrations_dir):
        print("✅ Миграции уже существуют")
        return True
    else:
        print("⚠️  Папка миграций пустая или отсутствует")
        
        # Создаем базовую миграцию
        try:
            print("🔄 Создаем начальную миграцию...")
            result = subprocess.run(["alembic", "revision", "--autogenerate", "-m", "initial_tables"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Начальная миграция создана")
                
                # Применяем миграцию
                print("🔄 Применяем миграцию...")
                result = subprocess.run(["alembic", "upgrade", "head"], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ Миграция применена успешно")
                    return True
                else:
                    print(f"❌ Ошибка применения миграции: {result.stderr}")
                    return False
            else:
                print(f"❌ Ошибка создания миграции: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"💥 Ошибка выполнения команды alembic: {e}")
            print("ℹ️  Убедитесь что alembic установлен: pip install alembic")
            return False

if __name__ == "__main__":
    check_and_create_migrations()
