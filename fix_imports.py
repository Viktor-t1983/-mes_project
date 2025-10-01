#!/usr/bin/env python3
"""Точечное исправление импортов в main.py"""

print("🔧 ИСПРАВЛЕНИЕ ИМПОРТОВ В MAIN.PY")
print("=" * 50)

# Читаем текущий main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Проверяем какие модели отсутствуют
missing_models = []
for model in ['ManufacturingOrder', 'DefectReport']:
    if f'from src.models.{model.lower()} import {model}' not in content:
        missing_models.append(model)

print(f"❌ Отсутствующие модели: {missing_models}")

if not missing_models:
    print("✅ Все модели уже импортированы!")
else:
    # Разбиваем на строки для точной вставки
    lines = content.split('\n')
    new_lines = []
    
    # Находим место для вставки - после других импортов моделей
    insert_position = None
    for i, line in enumerate(lines):
        new_lines.append(line)
        # Ищем последний импорт моделей
        if 'from src.models.' in line:
            insert_position = i + 1
    
    if insert_position:
        # Добавляем недостающие импорты
        for model in missing_models:
            import_line = f'from src.models.{model.lower()} import {model}'
            new_lines.insert(insert_position, import_line)
            print(f"✅ Добавлен импорт: {model}")
            insert_position += 1
        
        # Записываем обратно
        with open('main.py', 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print("✅ main.py успешно обновлен!")
    else:
        print("❌ Не удалось найти место для вставки импортов")

# Проверяем результат
print("\n🔍 ПРОВЕРКА РЕЗУЛЬТАТА:")
with open('main.py', 'r') as f:
    new_content = f.read()

for model in ['Employee', 'ManufacturingOrder', 'Operation', 'DefectReport', 'Order', 'Project']:
    status = "✅" if f'from src.models.{model.lower()} import {model}' in new_content else "❌"
    print(f"   {status} {model}")

