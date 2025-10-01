import os
from dotenv import load_dotenv

load_dotenv()

def fix_database_url():
    print("🔧 ИСПРАВЛЕНИЕ DATABASE_URL")
    print("=" * 35)
    
    current_url = os.getenv("DATABASE_URL")
    print(f"Текущий DATABASE_URL: {current_url}")
    
    # Исправляем URL для psycopg2
    if current_url and "asyncpg" in current_url:
        fixed_url = current_url.replace("postgresql+asyncpg://", "postgresql://")
        print(f"Исправленный DATABASE_URL: {fixed_url}")
        
        # Обновляем .env файл
        with open(".env", "r") as f:
            content = f.read()
        
        content = content.replace(current_url, fixed_url)
        
        with open(".env", "w") as f:
            f.write(content)
        
        print("✅ .env файл обновлен")
        return fixed_url
    else:
        print("✅ DATABASE_URL уже в правильном формате")
        return current_url

if __name__ == "__main__":
    fixed_url = fix_database_url()
    print(f"\n📋 Для использования в скриптах: {fixed_url}")
