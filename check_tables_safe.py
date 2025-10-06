import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect('postgresql://postgres:MesProject2025@localhost/mes_db')
    for table in ['projects', 'orders']:
        # Валидация имени таблицы (только буквы и подчёркивания)
        assert table.replace('_', '').isalpha(), f"Недопустимое имя таблицы: {table}"
        cols = await conn.fetch(f"""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = '{table}' ORDER BY ordinal_position
        """)
        print(f'✅ Таблица {table}: {[c["column_name"] for c in cols]}')
    await conn.close()

asyncio.run(main())
