# Создаем чистую версию main.py без ошибок форматирования
import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Удаляем все проблемные QR эндпоинты и создаем один чистый
# Находим и удаляем ВСЕ QR-эндпоинты
qr_patterns = [
    r'@app\.get\("/api/v1/qr/order/\{order_id\}"\)[\s\S]*?def get_order_qr[\s\S]*?return \{[\s\S]*?order_\{order_id\}"\}',
    r'# ========== QR CODE GENERATION ==========[\s\S]*?@app\.get\("/api/v1/qr/\{entity\}/\{id\}"\)[\s\S]*?def generate_qr_code[\s\S]*?return \{[\s\S]*?\}'
]

for pattern in qr_patterns:
    content = re.sub(pattern, '', content, flags=re.DOTALL)

# Добавляем один чистый QR эндпоинт в конец
clean_qr = '''
# ========== QR CODE GENERATION ==========
@app.get("/api/v1/qr/{entity}/{id}")
async def generate_qr_code(entity: str, id: int):
    """Генерация QR-кода для сущности"""
    valid_entities = ['order', 'employee', 'mo']
    if entity not in valid_entities:
        raise HTTPException(status_code=400, detail="Неподдерживаемая сущность")
    
    qr_data = f"{entity}_{id}_clean_{hash(f'{entity}{id}') % 10000:04d}"
    
    return {
        "message": f"QR-код для {entity} {id}",
        "entity": entity,
        "entity_id": id,
        "qr_data": qr_data
    }
'''

# Удаляем пустые строки и добавляем чистый QR эндпоинт
content = content.rstrip() + '\n\n' + clean_qr + '\n'

# Удаляем возможные дублирующиеся импорты
import re
content = re.sub(r'from src\.models\.\w+ import \w+\n+from src\.models\.\w+ import \w+', '', content)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Создана чистая версия main.py с одним QR эндпоинтом")
