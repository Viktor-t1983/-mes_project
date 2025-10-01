# Создаем надежную версию main.py с улучшенным управлением подключениями
import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Улучшаем функцию get_db для лучшего управления подключениями
new_get_db = '''
async def get_db():
    """Надежное получение сессии БД с обработкой ошибок"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
'''

# Заменяем старую функцию get_db
old_get_db_pattern = r'async def get_db\(\):[\s\S]*?await session\.close\(\)'
content = re.sub(old_get_db_pattern, new_get_db, content, flags=re.DOTALL)

# Добавляем health check эндпоинт для проверки БД
health_check = '''

# ========== HEALTH CHECK ==========
@app.get("/api/v1/health")
async def health_check():
    """Проверка здоровья системы и подключения к БД"""
    try:
        # Проверяем подключение к БД
        async with AsyncSessionLocal() as session:
            result = await session.execute("SELECT 1")
            db_status = "healthy" if result.scalar() == 1 else "unhealthy"
        
        return {
            "status": "healthy",
            "database": db_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "database": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
'''

# Добавляем health check перед QR эндпоинтами
content = content.replace('# ========== QR CODE GENERATION ==========', health_check + '\n# ========== QR CODE GENERATION ==========')

# Сохраняем улучшенную версию
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Создана надежная версия main.py")
print("   - Улучшено управление подключениями к БД")
print("   - Добавлен health check эндпоинт")
print("   - Добавлена обработка ошибок БД")
