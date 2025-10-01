# Исправляем ошибки форматирования в main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Исправляем проблему с отступами - находим и исправляем неправильные отступы
import re

# Ищем строки с проблемами отступов (строки которые могут быть сломанными)
lines = content.split('\n')
fixed_lines = []

for i, line in enumerate(lines):
    # Исправляем строки которые выглядят сломанными
    if line.strip().startswith('{id}","') and line.count('"') % 2 != 0:
        # Это сломанная строка - удаляем ее
        continue
    elif line.strip() == '          ^' or 'IndentationError' in line:
        # Удаляем строки с ошибками
        continue
    else:
        fixed_lines.append(line)

# Собираем обратно
fixed_content = '\n'.join(fixed_lines)

# Удаляем дублирующиеся QR эндпоинты если есть
# Оставляем только последний (самый простой) QR эндпоинт
qr_pattern = r'# ========== QR CODE GENERATION ==========[\s\S]*?@app\.get\("/api/v1/qr/\{entity\}/\{id\}"\)[\s\S]*?def generate_qr_code[\s\S]*?return \{[\s\S]*?\}'

# Находим все QR эндпоинты
qr_matches = list(re.finditer(qr_pattern, fixed_content, re.DOTALL))

if len(qr_matches) > 1:
    # Оставляем только последний
    last_qr = qr_matches[-1]
    # Удаляем все кроме последнего
    for match in qr_matches[:-1]:
        fixed_content = fixed_content.replace(match.group(0), '')

# Сохраняем исправленный файл
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Ошибки форматирования исправлены")
print("✅ Дублирующиеся QR эндпоинты удалены")
