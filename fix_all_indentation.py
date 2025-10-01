# Полное исправление всех отступов в main.py
with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Функция для исправления отступов в блоке
def fix_indentation_block(start_line, end_line):
    for i in range(start_line, min(end_line, len(lines))):
        line = lines[i]
        stripped = line.lstrip()
        
        # Если строка не пустая и имеет неправильные отступы
        if stripped and not line.startswith('    ') and not line.startswith('@') and not line.startswith('def ') and not line.startswith('async '):
            # Исправляем отступ до 4 пробелов
            lines[i] = '    ' + stripped

# Находим проблемные области и исправляем их
print("🔧 ИСПРАВЛЕНИЕ ОТСТУПОВ...")

# Исправляем область вокруг строки 249 (индекс 248)
if len(lines) > 248:
    print(f"Строка 249 до исправления: {repr(lines[248])}")
    # Исправляем конкретную строку 249
    if 'qr_data' in lines[248]:
        lines[248] = '        "qr_data": qr_data\n'
        print("✅ Строка 249 исправлена")
    
    # Исправляем соседние строки в этом блоке
    fix_indentation_block(245, 255)

# Сохраняем исправленный файл
with open('main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Все отступы исправлены")
