#!/usr/bin/env python3
"""
FULL DB AUDIT: Проверка структуры всех таблиц MES-системы
Сравнивает текущую БД с требованиями Дней 1–6.
"""
import asyncio
import asyncpg

# Требуемая структура таблиц (на основе ТЗ и реализации)
REQUIRED_TABLES = {
    "operations": [
        "id", "manufacturing_order_id", "operation_number", "name", "description",
        "planned_duration", "actual_duration", "status", "assigned_employee_id",
        "started_at", "completed_at", "quality_check_passed", "notes", "created_at",
        "operation_type", "workcenter_id", "machine_id",
        "pause_duration", "pause_events", "planned_start", "planned_end",
        "actual_start", "actual_end"
    ],
    "manufacturing_orders": [
        "id", "order_id", "part_number", "status", "current_operation_id",
        "created_at", "updated_at"
    ],
    "machines": [
        "id", "name", "type", "location", "status", "last_heartbeat", "machine_token", "technical_docs"
    ],
    "employees": [
        "id", "first_name", "last_name", "qr_code", "role", "allowed_workcenters", "is_active"
    ],
    "audit_log": [
        "id", "user_id", "machine_id", "action", "ip_address", "timestamp", "data_snapshot"
    ]
}

async def main():
    conn = await asyncpg.connect(
        user='postgres',
        password='MesProject2025',
        database='mes_db',
        host='localhost'
    )
    
    print("=" * 70)
    print("🔍 FULL DB AUDIT: Проверка структуры таблиц MES")
    print("=" * 70)
    
    for table_name, required_columns in REQUIRED_TABLES.items():
        print(f"\n📋 Таблица: {table_name}")
        
        # Получаем текущие колонки
        current_columns = await conn.fetch("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = $1 ORDER BY ordinal_position
        """, table_name)
        current_set = {row['column_name'] for row in current_columns}
        
        if not current_columns:
            print(f"  ❌ Таблица НЕ СУЩЕСТВУЕТ")
            continue
        
        print(f"  ✅ Найдено колонок: {len(current_columns)}")
        
        # Проверяем недостающие колонки
        missing = set(required_columns) - current_set
        if missing:
            print(f"  ⚠️  Отсутствуют колонки: {', '.join(sorted(missing))}")
            print(f"  💡 Команда для добавления:")
            for col in sorted(missing):
                if col in ["pause_events"]:
                    col_type = "JSONB"
                elif col in ["planned_start", "planned_end", "actual_start", "actual_end", "last_heartbeat", "timestamp", "created_at", "updated_at"]:
                    col_type = "TIMESTAMP WITH TIME ZONE"
                elif col in ["quality_check_passed", "is_active"]:
                    col_type = "BOOLEAN"
                elif col in ["pause_duration", "planned_duration", "actual_duration", "operation_number"]:
                    col_type = "INTEGER"
                else:
                    col_type = "VARCHAR"
                print(f"      ALTER TABLE {table_name} ADD COLUMN {col} {col_type};")
        else:
            print(f"  ✅ Все колонки на месте")
    
    await conn.close()
    print("\n" + "=" * 70)
    print("✅ АУДИТ ЗАВЕРШЁН")
    print("💡 Используйте команды выше для исправления структуры БД")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
