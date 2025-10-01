# Исправляем эндпоинт QR-кодов для работы с employee и mo
import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим текущий эндпоинт QR-кодов и заменяем его
old_qr_pattern = r'@app\.get\("/api/v1/qr/\{entity\}/\{id\}"\)[\s\S]*?def generate_qr_code[\s\S]*?return \{[\s\S]*?\}'

new_qr_endpoint = '''
@app.get("/api/v1/qr/{entity}/{id}")
async def generate_qr_code(entity: str, id: int, db: AsyncSession = Depends(get_db)):
    """
    Генерация QR-кода для сущности (order, employee, mo)
    """
    valid_entities = ['order', 'employee', 'mo']
    if entity not in valid_entities:
        raise HTTPException(status_code=400, detail=f"Неподдерживаемая сущность. Допустимо: {valid_entities}")
    
    # Проверяем существование сущности в базе данных
    if entity == 'order':
        result = await db.execute(select(Order).where(Order.id == id))
    elif entity == 'employee':
        result = await db.execute(select(Employee).where(Employee.id == id))
    elif entity == 'mo':
        result = await db.execute(select(ManufacturingOrder).where(ManufacturingOrder.id == id))
    
    entity_obj = result.scalar_one_or_none()
    
    if not entity_obj:
        raise HTTPException(status_code=404, detail=f"{entity.capitalize()} с ID {id} не найден")
    
    # Генерируем QR-данные
    qr_data = f"{entity}_{id}_{hash(f'{entity}{id}') % 10000:04d}"
    
    return {
        "message": f"QR-код для {entity} {id}",
        "entity": entity,
        "entity_id": id,
        "entity_name": getattr(entity_obj, 'product_name', getattr(entity_obj, 'first_name', getattr(entity_obj, 'order_number', 'Unknown'))),
        "qr_data": qr_data,
        "qr_image_url": f"/api/v1/qr/image/{qr_data}"  # В реальной системе здесь был бы URL изображения
    }
'''

# Заменяем старый эндпоинт на новый
if re.search(old_qr_pattern, content):
    content = re.sub(old_qr_pattern, new_qr_endpoint, content, flags=re.DOTALL)
    print("✅ Эндпоинт QR-кодов обновлен")
else:
    print("❌ Не удалось найти эндпоинт QR-кодов для замены")

# Сохраняем изменения
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("🔧 Исправления применены к эндпоинту QR-кодов")
