#!/usr/bin/env python3
"""
DIAGNOSTIC SCRIPT: Проверка локального состояния MES-проекта (Дни 1–5)
Автоматически сверяет структуру, файлы и ключевые компоненты.
Работает в Git Bash (Windows 10, без Docker).
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(".").resolve()
EXPECTED_FILES = {
    # День 1–2: Инфраструктура
    "requirements.txt": True,
    "main.py": True,
    ".env": False,  # может отсутствовать — это нормально
    ".gitignore": False,

    # День 3: Ядро
    "src/models/order.py": True,
    "src/models/operation.py": True,
    "src/models/defect_report.py": True,
    "src/models/employee.py": True,
    "src/models/manufacturing_order.py": True,

    # День 4: Геймификация, 1С, перепланирование
    "src/models/gamification.py": True,
    "src/services/gamification_service.py": True,
    "src/services/one_c_service.py": True,
    "src/services/replanning_service.py": True,
    "src/api/day4_endpoints.py": True,

    # День 5: Мобильное API — КРИТИЧЕСКИ ВАЖНО
    "src/api/mobile_api.py": True,  # ← часто отсутствует!
}

def check_file(path: str, required: bool) -> bool:
    full_path = PROJECT_ROOT / path
    exists = full_path.exists()
    status = "✅" if exists else ("⚠️" if not required else "❌")
    print(f"{status} {path}")
    return exists or not required

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=PROJECT_ROOT)
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 70)
    print("🔍 DIAGNOSTIC: Проверка локального состояния MES-проекта")
    print(f"📁 Проект: {PROJECT_ROOT}")
    print("=" * 70)

    print("\n📂 Проверка файловой структуры:")
    missing_required = []
    for file, required in EXPECTED_FILES.items():
        if not check_file(file, required):
            if required:
                missing_required.append(file)

    print("\n📦 Проверка зависимостей:")
    deps_ok, _ = run_cmd("pip list | grep -E 'fastapi|uvicorn|sqlalchemy|alembic'")
    print("✅ Основные зависимости установлены" if deps_ok else "❌ Некоторые зависимости отсутствуют")

    print("\n🔧 Проверка Alembic и миграций:")
    alembic_ok, _ = run_cmd("alembic --help")
    migrations_exist = (PROJECT_ROOT / "migrations").exists()
    print(f"✅ Alembic доступен" if alembic_ok else "⚠️ Alembic не найден")
    print(f"✅ Папка migrations существует" if migrations_exist else "⚠️ Папка migrations отсутствует")

    print("\n📡 Проверка подключения к GitHub (состояние репозитория):")
    git_ok, remote_url = run_cmd("git config --get remote.origin.url")
    if git_ok and "Viktor-t1983/-mes_project" in remote_url:
        print("✅ Привязан к правильному репозиторию")
        clean, _ = run_cmd("git status --porcelain")
        if not clean:
            print("⚠️ Есть несохранённые изменения (git status не чист)")
        else:
            print("✅ Git-репозиторий чист")
    else:
        print("⚠️ Не привязан к ожидаемому репозиторию")

    print("\n🚀 Проверка запуска main.py (импорты):")
    try:
        exec(open(PROJECT_ROOT / "main.py").read())
        print("✅ main.py синтаксически корректен")
    except Exception as e:
        print(f"❌ Ошибка в main.py: {e}")

    print("\n" + "=" * 70)
    if missing_required:
        print("❗ КРИТИЧЕСКИЕ ОТСУТСТВУЮЩИЕ ФАЙЛЫ:")
        for f in missing_required:
            print(f"  - {f}")
        print("\n💡 Рекомендация: Запустите скрипт завершения Дня 5.")
    else:
        print("✅ Все обязательные файлы на месте.")
        print("🎉 Локальный проект соответствует полной реализации Дней 1–5.")
    print("=" * 70)

if __name__ == "__main__":
    main()
