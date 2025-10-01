#!/usr/bin/env python3
"""Исправление проблем с импортами"""

import re

print("🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМ С ИМПОРТАМИ")
print("=" * 50)

# Читаем текущий main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Текущие импорты моделей:")
imports = re.findall(r'from src\.models\.(\w+) import (\w+)', content)
for module, model in imports:
    print(f"   from src.models.{module} import {model}")

# Правильные имена файлов (с подчеркиваниями)
correct_mappings = {
    'manufacturingorder': 'manufacturing_order',
    'defectreport': 'defect_report'
}

# Исправляем неправильные импорты
fixed_content = content
for wrong, correct in correct_mappings.items():
    if f'from src.models.{wrong} import' in fixed_content:
        fixed_content = fixed_content.replace(
            f'from src.models.{wrong} import', 
            f'from src.models.{correct} import'
        )
        print(f"✅ Исправлен: {wrong} -> {correct}")

# Записываем исправленный файл
if fixed_content != content:
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    print("✅ main.py исправлен")
else:
    print("✅ Импорты уже правильные")

# Проверяем результат
print("\n🔍 ПРОВЕРКА ИСПРАВЛЕННЫХ ИМПОРТОВ:")
with open('main.py', 'r') as f:
    new_content = f.read()

imports = re.findall(r'from src\.models\.(\w+) import (\w+)', new_content)
for module, model in imports:
    status = "✅" if '_' in module or module in ['employee', 'operation', 'order', 'project'] else "❌"
    print(f"   {status} from src.models.{module} import {model}")

