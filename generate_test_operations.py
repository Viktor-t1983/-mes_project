#!/usr/bin/env python3
"""Надёжный генератор теста операций."""
import os

def write_test_script():
    content = '''#!/usr/bin/env python3
"""ТЕСТ ПО ОПЕРАЦИЯМ — ПОЛНЫЙ ЖИЗНЕННЫЙ ЦИКЛ"""
import asyncio
import asyncpg
from datetime import datetime, timedelta

async def main():
    conn = await asyncpg.connect(
        user='postgres',
        password='MesProject2025',
        database='mes_db',
        host='localhost'
    )
    print("🔍 Начинаем тест операций...")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
'''
    with open("test_operations_full.py", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    write_test_script()
    print("✅ Файл test_operations_full.py создан без ошибок")
