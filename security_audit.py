#!/usr/bin/env python3
"""Финальный аудит безопасности перед запуском в production"""

import os
import sys

def check_env_secrets():
    """Проверка, что секреты не в коде"""
    secrets = ["MesProject2025", "your-secret-key"]
    with open("src/core/config.py", "r") as f:
        content = f.read()
        for secret in secrets:
            if secret in content:
                print(f"❌ Найден секрет в коде: {secret}")
                return False
    print("✅ Секреты вынесены в .env")
    return True

def check_gitignore():
    """Проверка .gitignore"""
    required = [".env", "venv/", "__pycache__/"]
    with open(".gitignore", "r") as f:
        content = f.read()
        for item in required:
            if item not in content:
                print(f"❌ Отсутствует в .gitignore: {item}")
                return False
    print("✅ .gitignore корректен")
    return True

if __name__ == "__main__":
    print("🔒 ФИНАЛЬНЫЙ SECURITY AUDIT")
    print("=" * 40)
    ok = check_env_secrets() and check_gitignore()
    if ok:
        print("\n🎉 СИСТЕМА ГОТОВА К ЗАПУСКУ В PRODUCTION")
        sys.exit(0)
    else:
        print("\n🚨 ИСПРАВЬТЕ ОШИБКИ ПЕРЕД ЗАПУСКОМ")
        sys.exit(1)
