# Исправляем проблему с подключением к БД в main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем обработку ошибок подключения к БД
import re

# Находим все функции с db.execute и добавляем обработку ошибок
functions_to_fix = [
    'get_orders',
    'get_manufacturing_orders', 
    'get_employees',
    'get_operations',
    'get_defects',
    'get_projects'
]

for func_name in functions_to_fix:
    # Находим функцию
    pattern = rf'async def {func_name}\([^)]*db[^)]*\):[\s\S]*?return [^\n]+'
    match = re.search(pattern, content)
    
    if match:
        old_function = match.group(0)
        
        # Добавляем обработку ошибок
        new_function = old_function.replace(
            'result = await db.execute(',
            'try:\n        result = await db.execute('
        ).replace(
            'return ',
            'except Exception as e:\n        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {e}")\n    return '
        )
        
        content = content.replace(old_function, new_function)
        print(f"✅ Добавлена обработка ошибок для {func_name}")

# Сохраняем исправленный файл
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Обработка ошибок БД добавлена")
