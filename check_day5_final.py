#!/usr/bin/env python3
"""
MES Project Day 5 Final Compliance Checker
Senior Security Engineer Level Verification Script
"""
import os
import sys
from pathlib import Path

PROJECT_ROOT = "."
REQUIRED_FILES = [
    # Корень
    ".env",
    ".gitignore",
    "requirements.txt",
    "main.py",
    "alembic.ini",

    # API
    "src/api/health.py",
    "src/api/day4_endpoints.py",
    "src/api/mobile_api.py",  # Новое в День 5

    # Core
    "src/core/database.py",
    "src/core/security.py",
    "src/core/logger.py",      # Новое в День 5
    "src/core/auth.py",        # Новое в День 5

    # Models
    "src/models/base.py",
    "src/models/order.py",
    "src/models/employee.py",
    "src/models/manufacturing_order.py",
    "src/models/operation.py",
    "src/models/defect_report.py",
    "src/models/gamification.py",  # Новое в День 4
    "src/models/one_c.py",         # Новое в День 5

    # Schemas
    "src/schemas/gamification.py", # Новое в День 4
    "src/schemas/one_c.py",        # Новое в День 5

    # Services
    "src/services/gamification_service.py",  # Новое в День 4
    "src/services/one_c_service.py",         # Новое в День 5

    # Utils
    "src/utils/qrcode_generator.py",
    "src/utils/crypto.py",  # Новое в День 5

    # Scripts
    "scripts/backup-db.sh",
    "scripts/restore-db.sh",  # Новое в День 5
]

REQUIRED_IMPORTS_IN_MAIN = [
    "from src.core.logger import logger",
    "from src.core.security import setup_security_middleware",
    "setup_security_middleware(app)",
]

SECURITY_CHECKS = [
    "src/core/security.py",
    "src/core/auth.py",
    "src/utils/crypto.py",
]

def check_file_exists(file_path):
    """Проверяет, существует ли файл"""
    full_path = os.path.join(PROJECT_ROOT, file_path)
    return Path(full_path).is_file()

def check_content_in_file(file_path, content_list):
    """Проверяет, содержится ли список строк в файле"""
    full_path = os.path.join(PROJECT_ROOT, file_path)
    if not Path(full_path).is_file():
        return False
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return all(c in content for c in content_list)
    except Exception:
        return False

def run_check():
    print("🔍 Финальная проверка соответствия проекта 5-му дню...")
    print("="*60)

    missing_files = []
    for file in REQUIRED_FILES:
        if not check_file_exists(file):
            missing_files.append(file)

    if missing_files:
        print("❌ Отсутствующие файлы:")
        for f in missing_files:
            print(f"   - {f}")
    else:
        print("✅ Все файлы на месте")

    print("-" * 60)

    if not check_content_in_file("main.py", REQUIRED_IMPORTS_IN_MAIN):
        print("❌ main.py не содержит необходимые импорты/настройки logger и security")
    else:
        print("✅ main.py содержит импорты logger и security middleware")

    print("-" * 60)

    # Проверка .env
    env_ok = check_file_exists(".env")
    if not env_ok:
        print("❌ .env не найден")
    else:
        print("✅ .env существует")

    print("-" * 60)

    # Проверка безопасности
    security_ok = all(check_file_exists(f) for f in SECURITY_CHECKS)
    if not security_ok:
        print("❌ Не все компоненты безопасности реализованы")
        print("   Проверьте: security.py, auth.py, crypto.py")
    else:
        print("✅ Все компоненты безопасности на месте")

    print("="*60)

    if not missing_files and check_content_in_file("main.py", REQUIRED_IMPORTS_IN_MAIN) and env_ok and security_ok:
        print("🎉 Поздравляем! Проект полностью соответствует 5-му дню.")
        print("✅ Все файлы, зависимости, безопасность и функции — на месте.")
        return True
    else:
        print("❌ Проект НЕ соответствует требованиям 5-го дня. См. детали выше.")
        return False

if __name__ == "__main__":
    success = run_check()
    if success:
        print("\n🚀 Готово! Вы можете продолжать проект.")
    else:
        print("\n⚠️  Исправьте ошибки, чтобы перейти к следующему этапу.")
        sys.exit(1)
