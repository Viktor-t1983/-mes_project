import os

def create_clean_env():
    print("🛠️ СОЗДАНИЕ ЧИСТОГО .env ФАЙЛА")
    print("=" * 40)
    
    # Создаем чистый .env файл
    env_content = '''# PostgreSQL Database
DATABASE_URL=postgresql+asyncpg://postgres:MesProject2025@localhost:5432/mes_db

# Security
SECRET_KEY=your-secret-key-for-development-only-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=true
'''

    # Записываем файл в правильной кодировке
    with open('.env', 'w', encoding='utf-8', newline='\n') as f:
        f.write(env_content)
    
    print("✅ .env файл пересоздан с правильной кодировкой")
    print("📋 Содержимое:")
    print(env_content)

if __name__ == "__main__":
    create_clean_env()
