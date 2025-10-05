#!/usr/bin/env python3
import asyncio
import asyncpg
import json
from datetime import datetime, timedelta

async def main():
    conn = await asyncpg.connect(
        user='postgres',
        password='MesProject2025',
        database='mes_db',
        host='localhost'
    )
    print("🔍 Начинаем тест операций...")

    # Подготовка
    await conn.execute(
        "INSERT INTO manufacturing_orders (id, order_number, product_name, product_code, quantity, status) VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT (id) DO NOTHING",
        9999, "TEST-ORDER-001", "Тестовое изделие", "TEST-PROD-001", 10, "in_progress"
    )
    await conn.execute(
        "INSERT INTO machines (id, name, type, machine_token, location) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (id) DO NOTHING",
        9999, "Тестовый станок", "test", "op_test_token", "Цех Тест"
    )
    await conn.execute(
        "INSERT INTO employees (id, first_name, last_name, qr_code, role, is_active) VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT (id) DO NOTHING",
        9999, "Тест", "Оператор", "TEST_EMP_QR", "operator", True
    )
    print("✅ Подготовка завершена")

    # Создание операции
    now = datetime.utcnow()
    await conn.execute("""
        INSERT INTO operations (
            manufacturing_order_id, operation_number, name, status,
            assigned_employee_id, machine_id,
            planned_start, planned_end, planned_duration,
            operation_type, workcenter_id
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
    """, 9999, 1, "Тестовая операция", "in_progress", 9999, 9999, now - timedelta(minutes=10), now + timedelta(minutes=50), 60, "test_op", "workcenter_test")

    op_id = await conn.fetchval("SELECT id FROM operations WHERE manufacturing_order_id = 9999 ORDER BY id DESC LIMIT 1")
    print(f"✅ Операция создана: ID={op_id}")

    # Пауза — БЕЗ КОНКАТЕНАЦИИ
    pause_event = [{"start": (now + timedelta(minutes=5)).isoformat(), "reason": "Обед"}]
    await conn.execute("""
        UPDATE operations SET
            pause_events = $1,
            pause_duration = 15,
            status = 'paused'
        WHERE id = $2
    """, json.dumps(pause_event), op_id)
    print("⏸️  Операция на паузе")

    # Продолжение
    await conn.execute("UPDATE operations SET status = 'in_progress' WHERE id = $1", op_id)
    print("▶️  Операция продолжена")

    # Завершение
    await conn.execute("""
        UPDATE operations SET
            actual_start = $1,
            actual_end = $2,
            actual_duration = EXTRACT(EPOCH FROM ($2 - $1)) / 60,
            status = 'completed',
            quality_check_passed = true
        WHERE id = $3
    """, now, now + timedelta(minutes=45), op_id)
    print("✅ Операция завершена")

    # Проверка чистого времени
    clean_time = await conn.fetchval("SELECT actual_duration - pause_duration FROM operations WHERE id = $1", op_id)
    print(f"⏱️  Чистое время: {clean_time:.1f} мин")

    await conn.close()
    print("📊 Тест завершён")

if __name__ == "__main__":
    asyncio.run(main())
