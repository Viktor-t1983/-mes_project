#!/usr/bin/env python3
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
    print("🔧 Подготовка данных для OEE...")

    # Убедимся, что станок существует
    await conn.execute("""
        INSERT INTO machines (id, name, type, machine_token, location)
        VALUES (9999, 'Тестовый станок OEE', 'test', 'oee_test_token', 'Цех Тест')
        ON CONFLICT (id) DO NOTHING
    """)

    # Убедимся, что MO существует
    await conn.execute("""
        INSERT INTO manufacturing_orders (id, order_number, product_name, product_code, quantity, status)
        VALUES (9999, 'OEE-TEST-001', 'Тестовое изделие', 'OEE-PART-001', 1, 'in_progress')
        ON CONFLICT (id) DO NOTHING
    """)

    # Добавим операцию за последние 24 часа
    now = datetime.utcnow()
    await conn.execute("""
        INSERT INTO operations (
            manufacturing_order_id, operation_number, name, status,
            machine_id, planned_start, planned_end, planned_duration,
            actual_start, actual_end, actual_duration, pause_duration
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
    """,
    9999, 1, "Тестовая операция OEE", "completed",
    9999,
    now - timedelta(hours=2), now - timedelta(minutes=30), 90,
    now - timedelta(hours=2), now - timedelta(minutes=30), 75, 15
    )

    print("✅ Тестовая операция добавлена")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
