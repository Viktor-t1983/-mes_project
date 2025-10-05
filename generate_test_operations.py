    await conn.execute("""
        INSERT INTO operations (
            manufacturing_order_id, operation_number, name, status,
            assigned_employee_id, machine_id,
            planned_start, planned_end, planned_duration,
            operation_type, workcenter_id
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
    """,
    9999, 1, "Тестовая операция", "in_progress",
    9999, 9999,
    now - timedelta(minutes=10), now + timedelta(minutes=50), 60,
    "test_op", "workcenter_test"
    )
    op_id = await conn.fetchval("SELECT id FROM operations WHERE manufacturing_order_id = 9999 ORDER BY id DESC LIMIT 1")
    print(f"✅ Операция создана: ID={op_id}")

    # === 3. Пауза ===
    await conn.execute("""
        UPDATE operations SET
            pause_events = '[{"start": "' || $1 || '", "reason": "Обед"}]',
            pause_duration = 15,
            status = 'paused'
        WHERE id = $2
    """, (now + timedelta(minutes=5)).isoformat(), op_id)
    print("⏸️  Операция поставлена на паузу (Обед, 15 мин)")

    # === 4. Продолжение ===
    await conn.execute("UPDATE operations SET status = 'in_progress' WHERE id = $1", op_id)
    print("▶️  Операция продолжена")

    # === 5. Завершение ===
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

    # === 6. Проверка чистого времени ===
    clean_time = await conn.fetchval("""
        SELECT actual_duration - pause_duration FROM operations WHERE id = $1
    """, op_id)
    print(f"⏱️  Чистое время операции: {clean_time:.1f} мин")

    # === 7. Добавим вторую операцию для OEE ===
    await conn.execute("""
        INSERT INTO operations (
            manufacturing_order_id, operation_number, name, status,
            assigned_employee_id, machine_id,
            planned_start, planned_end, planned_duration,
            pause_duration, operation_type, workcenter_id
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
    """,
    9999, 2, "Вторая тестовая операция", "completed",
    9999, 9999,
    now - timedelta(hours=1), now, 40,
    0, "test_op", "workcenter_test"
    )

    print("📊 Тест завершён. Проверьте OEE: curl http://localhost:8000/api/v1/iiot/oee/9999")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
'''
    with open("test_operations_full.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Файл test_operations_full.py создан без ошибок")

if __name__ == "__main__":
    write_test_script()
