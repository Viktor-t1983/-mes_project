# Исправляем конкретную ошибку на строке 261
with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Находим и исправляем проблемную строку 261
for i in range(len(lines)):
    if i == 260:  # Строка 261 (индексация с 0)
        print(f"Исходная строка 261: {repr(lines[i])}")
        # Если строка содержит ошибку форматирования, исправляем ее
        if '{id}"' in lines[i] and lines[i].strip() == '{id}",':
            lines[i] = '        "qr_data": qr_data\n'
            print("✅ Строка 261 исправлена")
        elif lines[i].strip() == '          ^':
            lines[i] = ''
            print("✅ Удалена строка с ошибкой")
        else:
            # Просто проверяем отступы
            if not lines[i].startswith('    ') and len(lines[i].strip()) > 0:
                lines[i] = '    ' + lines[i].lstrip()
                print("✅ Исправлены отступы строки 261")

# Сохраняем исправленный файл
with open('main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Исправления применены к строке 261")
