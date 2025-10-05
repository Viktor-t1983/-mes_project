import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        user='postgres',
        password='MesProject2025',
        database='mes_db',
        host='localhost'
    )
    tables = await conn.fetch("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name IN ('machines', 'audit_log')
        ORDER BY table_name;
    """)
    print("✅ Таблицы Дня 6:")
    for row in tables:
        print(f" - {row['table_name']}")
    await conn.close()

asyncio.run(main())
