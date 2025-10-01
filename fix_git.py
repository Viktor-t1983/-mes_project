#!/usr/bin/env python3
"""Исправление Git статуса"""

import subprocess
import os

print("🔧 ИСПРАВЛЕНИЕ GIT СТАТУСА")
print("=" * 50)

# Проверяем текущий статус
print("1. Текущий Git статус:")
result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
print(result.stdout)

if result.stdout.strip():
    print("2. Добавляем изменения в Git...")
    subprocess.run(['git', 'add', '.'], check=True)
    
    print("3. Создаем коммит...")
    commit_msg = "🔧 Fix: Add missing models ManufacturingOrder and DefectReport to main.py"
    subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
    
    print("4. Отправляем в GitHub...")
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print("✅ Изменения отправлены в GitHub")
else:
    print("✅ Git репозиторий чист")

# Проверяем финальный статус
print("\n5. Финальный Git статус:")
result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
if result.stdout.strip():
    print("❌ Остались изменения:")
    print(result.stdout)
else:
    print("✅ Репозиторий полностью чист!")

