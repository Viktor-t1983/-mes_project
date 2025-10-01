import os
import re

# Читаем текущий main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем импорт БД на исправленную версию
content = content.replace('from database import engine, AsyncSessionLocal, Base, get_db', 'from fix_database_connection import engine, AsyncSessionLocal, Base, get_db')

# Добавляем обработку ошибок для всех эндпоинтов с БД
error_handling_code = '''
from fastapi import HTTPException
import traceback
'''

# Добавляем импорт обработки ошибок если его нет
if 'from fastapi import HTTPException' not in content:
    content = content.replace('from fastapi import FastAPI', 'from fastapi import FastAPI, HTTPException')

# Добавляем обработку ошибок для каждой функции с БД
functions_to_protect = [
    'get_orders', 'get_manufacturing_orders', 'get_employees', 
    'get_operations', 'get_defects', 'get_projects'
]

for func_name in functions_to_protect:
    pattern = f'async def {func_name}\(.*?\):(.*?)(?=\\n\\nasync def|\\n@app|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        func_body = match.group(1)
        # Проверяем нет ли уже обработки ошибок
        if 'try:' not in func_body and 'except' not in func_body:
            # Добавляем обработку ошибок
            protected_body = f'''
    try:
{func_body}
    except Exception as e:
        print(f"Database error in {func_name}: {{e}}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error: {{str(e)}}")
'''
            content = content.replace(func_body, protected_body)

# Сохраняем обновленный файл
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Main.py updated with fixed database connection and error handling")
