#!/usr/bin/env python3
"""
Самодиагностический скрипт для проверки синтаксиса Python-файлов.
"""
import ast
import os
import sys

def check_file_syntax(filepath):
    """Проверяет синтаксис одного файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source, filename=filepath)
        print(f"✅ {filepath}")
        return True
    except SyntaxError as e:
        print(f"❌ {filepath}:{e.lineno}:{e.offset} — {e.msg}")
        return False
    except Exception as e:
        print(f"⚠️  {filepath} — {e}")
        return False

def main():
    project_root = "."
    error_count = 0
    total_count = 0

    print("🔍 Проверка синтаксиса всех Python-файлов...\n")

    for root, _, files in os.walk(project_root):
        for file in files:
            if file.endswith(".py") and "venv" not in root:
                filepath = os.path.join(root, file)
                total_count += 1
                if not check_file_syntax(filepath):
                    error_count += 1

    print(f"\n📊 Итог: {total_count - error_count}/{total_count} файлов без ошибок")
    if error_count > 0:
        print("🚨 Найдены синтаксические ошибки. Исправьте их перед запуском сервера.")
        sys.exit(1)
    else:
        print("🎉 Все файлы синтаксически корректны.")

if __name__ == "__main__":
    main()
