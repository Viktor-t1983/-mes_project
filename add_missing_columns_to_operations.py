import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        user='postgres',
        password='MesProject2025',
        database='mes_db',
        host='localhost'
    )
    
    # Список колонок для добавления
    missing_columns = [
        ("pause_duration", "INTEGER DEFAULT 0"),
        ("pause_events", "JSONB DEFAULT '[]'::jsonb"),
        ("planned_start", "TIMESTAMP WITH TIME ZONE"),
        ("planned_end", "TIMESTAMP WITH TIME ZONE"),
        ("actual_start", "TIMESTAMP WITH TIME ZONE"),
        ("actual_end", "TIMESTAMP WITH TIME ZONE")
    ]
    
    for column_name, column_type in missing_columns:
        # Проверяем, существует ли колонка
        exists = await conn.fetchval("""
            SELECT 1 FROM information_schema.columns
            WHERE table_name = 'operations' AND column_name = $1
        """, column_name)
        
        if not exists:
            await conn.execute(f"""
                ALTER TABLE operations ADD COLUMN {column_name} {column_type}
            """)
            print(f"✅ Добавлена колонка: {column_name}")
        else:
            print(f"ℹ️ Колонка уже существует: {column_name}")
    
    await conn.close()

asyncio.run(main())
