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

    # Убедимся, что MO и станок существуют
    await conn.execute("INSERT INTO manufacturing_orders (id, order_id, status, part_number) VALUES (999, 1, 'planned', 'TEST') ON CONFLICT DO NOTHING")
    await conn.execute("INSERT INTO machines (id, name, type, machine_token) VALUES (999, 'Test Machine', 'test', 'test_token_999') ON CONFLICT DO NOTHING")

    # Добавляем операцию с данными для OEE
    now = datetime.utcnow()
    await conn.execute("""
        INSERT INTO operations (
            manufacturing_order_id, operation_number, name, status,
            assigned_employee_id, started_at, completed_at,
            planned_duration, actual_duration,
            operation_type, workcenter_id, machine_id,
            pause_duration, planned_start, planned_end
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
    """,
    999, 1, "Test OEE Operation", "completed",
    1, now - timedelta(hours=2), now - timedelta(hours=1),
    60, 55,
    "test", "wc_1", 999,
    5, now - timedelta(hours=3), now - timedelta(minutes=30)
    )

    print("✅ Тестовая операция для OEE добавлена")
    await conn.close()

asyncio.run(main())
