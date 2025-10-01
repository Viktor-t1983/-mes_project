#!/usr/bin/env python3
"""Финальное исправление Git статуса"""

import subprocess
import os

print("🔧 ФИНАЛЬНАЯ СИНХРОНИЗАЦИЯ С GIT")
print("=" * 50)

# Проверяем текущий статус
print("1. Текущий Git статус:")
result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, encoding='utf-8')
if result.stdout.strip():
    print("Изменения:")
    for line in result.stdout.strip().split('\n'):
        print(f"   {line}")
else:
    print("   ✅ Репозиторий чист")

# Добавляем все изменения
print("2. Добавляем изменения в Git...")
subprocess.run(['git', 'add', '.'], check=True)

# Проверяем что добавилось
result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, encoding='utf-8')
if result.stdout.strip():
    print("Изменения для коммита:")
    for line in result.stdout.strip().split('\n'):
        print(f"   {line}")
    
    # Создаем коммит
    print("3. Создаем коммит...")
    commit_msg = """🔧 Fix: Correct model imports and clean up

✅ Fixed ManufacturingOrder and DefectReport imports
✅ All 6 models properly imported
✅ CORS middleware working
✅ .env.example created
✅ Project ready for Day 4"""
    
    subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
    print("   ✅ Коммит создан")
    
    # Пушим в GitHub
    print("4. Отправляем в GitHub...")
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print("   ✅ Изменения отправлены в GitHub")
else:
    print("   ✅ Нет изменений для коммита")

# Финальная проверка
print("5. Финальная проверка Git...")
result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, encoding='utf-8')
if result.stdout.strip():
    print("❌ Остались изменения:")
    print(result.stdout)
else:
    print("✅ Репозиторий полностью чист!")

# Проверяем синхронизацию с GitHub
print("6. Проверка синхронизации с GitHub...")
try:
    subprocess.run(['git', 'fetch', 'origin'], capture_output=True)
    local = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    remote = subprocess.run(['git', 'rev-parse', 'origin/main'], capture_output=True, text=True).stdout.strip()
    if local == remote:
        print("   ✅ Полностью синхронизирован с GitHub")
    else:
        print("   ❌ Не синхронизирован с GitHub")
except:
    print("   ❌ Ошибка проверки GitHub")

