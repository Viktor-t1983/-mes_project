#!/usr/bin/env python3
"""Проверка существующих файлов моделей"""

import os
from pathlib import Path

print("🔍 ПРОВЕРКА ФАЙЛОВ МОДЕЛЕЙ")
print("=" * 50)

models_dir = Path('src/models')
if models_dir.exists():
    print("📁 Файлы в src/models/:")
    for file in models_dir.glob('*.py'):
        if file.name != '__init__.py':
            print(f"   ✅ {file.name}")
else:
    print("❌ Папка src/models/ не существует")

# Проверим main.py на правильность импортов
print("\n🔍 ПРОВЕРКА ИМПОРТОВ В MAIN.PY:")
with open('main.py', 'r') as f:
    content = f.read()

# Ищем все импорты моделей
import re
imports = re.findall(r'from src\.models\.(\w+) import (\w+)', content)
print("Найденные импорты:")
for module, model in imports:
    print(f"   from src.models.{module} import {model}")

# Проверим соответствие имен файлов
expected_files = {
    'employee': 'employee.py',
    'manufacturing_order': 'manufacturing_order.py', 
    'operation': 'operation.py',
    'defect_report': 'defect_report.py',
    'order': 'order.py',
    'project': 'project.py'
}

print("\n🔍 СООТВЕТСТВИЕ ИМЕН ФАЙЛОВ:")
for module, model in imports:
    expected_file = expected_files.get(module)
    actual_file = f"{module}.py"
    if models_dir.joinpath(actual_file).exists():
        print(f"   ✅ {actual_file} -> {model}")
    else:
        print(f"   ❌ {actual_file} -> {model} (файл не найден)")

