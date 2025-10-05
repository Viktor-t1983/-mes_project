import asyncio
import asyncpg
from datetime import datetime, timedelta

async def add_operation():
    conn = await asyncpg.connect(
        user='postgres',
        password='MesProject2025',
        database='mes_db',
        host='localhost',
        port=5432
    )

    # Убедимся, что станок с id=1 существует
    machine_exists = await conn.fetchval("SELECT 1 FROM machines WHERE id = 1")
    if not machine_exists:
        await conn.execute("""
            INSERT INTO machines (id, name, type, machine_token, location)
            VALUES (1, 'Тестовый станок', 'test', 'test_token', 'Цех 1')
            ON CONFLICT (id) DO NOTHING
        """)
        print("✅ Станок с id=1 создан")

    # Убедимся, что MO с id=1 существует
    mo_exists = await conn.fetchval("SELECT 1 FROM manufacturing_orders WHERE id = 1")
    if not mo_exists:
        await conn.execute("""
            INSERT INTO manufacturing_orders (id, order_id, status, part_number)
            VALUES (1, 1, 'planned', 'TEST-PART')
            ON CONFLICT (id) DO NOTHING
        """)
        print("✅ MO с id=1 создан")

    # Добавляем тестовую операцию
    now = datetime.utcnow()
    planned_start = now - timedelta(hours=1)

    await conn.execute("""
        INSERT INTO operations (
            machine_id, status, planned_start, pause_duration, 
            mo_id, operation_type, workcenter_id
        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT DO NOTHING
    """, 
    1,                          # machine_id
    "completed",               # status
    planned_start,             # planned_start
    5,                         # pause_duration
    1,                         # mo_id
    "test_operation",          # operation_type
    "workcenter_1"             # workcenter_id
    )
    
    print("✅ Тестовая операция добавлена")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(add_operation())
