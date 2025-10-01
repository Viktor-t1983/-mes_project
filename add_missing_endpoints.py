# Добавляем недостающие эндпоинты в main.py
import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем эндпоинт паузы операций
pause_operation_endpoint = '''
# ========== OPERATION PAUSE ==========
@app.post("/api/v1/operations/pause")
async def pause_operation(operation_id: int, db: AsyncSession = Depends(get_db)):
    """
    Поставить операцию на паузу
    """
    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    operation = result.scalar_one_or_none()
    
    if not operation:
        raise HTTPException(status_code=404, detail="Операция не найдена")
    
    if operation.status != 'in_progress':
        raise HTTPException(status_code=400, detail="Можно ставить на паузу только выполняющиеся операции")
    
    operation.status = 'paused'
    await db.commit()
    
    return {"message": f"Операция {operation_id} поставлена на паузу", "status": "paused"}
'''

# 2. Добавляем эндпоинт генерации QR-кодов
qr_code_endpoint = '''
# ========== QR CODE GENERATION ==========
@app.get("/api/v1/qr/{entity}/{id}")
async def generate_qr_code(entity: str, id: int, db: AsyncSession = Depends(get_db)):
    """
    Генерация QR-кода для сущности (order, employee, mo)
    """
    valid_entities = ['order', 'employee', 'mo']
    if entity not in valid_entities:
        raise HTTPException(status_code=400, detail=f"Неподдерживаемая сущность. Допустимо: {valid_entities}")
    
    # В реальной системе здесь была бы генерация QR-кода
    # Для демонстрации возвращаем текстовые данные
    qr_data = f"{entity}_{id}_{hash(f'{entity}{id}') % 10000:04d}"
    
    return {
        "message": f"QR-код для {entity} {id}",
        "entity": entity,
        "entity_id": id,
        "qr_data": qr_data,
        "qr_image_url": f"/api/v1/qr/image/{qr_data}"  # В реальной системе здесь был бы URL изображения
    }
'''

# Находим место для вставки после эндпоинта завершения операций
pattern = r'(@app\.post\("/api/v1/operations/complete"\)[^}]*?def operation_complete[^}]*?return \{[^}]*?\})'

def add_endpoints(match):
    original = match.group(0)
    return original + pause_operation_endpoint + qr_code_endpoint

# Заменяем в содержимом
content = re.sub(pattern, add_endpoints, content, flags=re.DOTALL)

# Сохраняем обновленный файл
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Недостающие эндпоинты добавлены в main.py")
print("   - POST /api/v1/operations/pause")
print("   - GET /api/v1/qr/{entity}/{id}")
