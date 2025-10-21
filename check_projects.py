import asyncio
import asyncpg

async def main():
    # Используем чистый postgresql:// для asyncpg
    conn = await asyncpg.connect('postgresql://postgres:MesProject2025@localhost/mes_db')
    cols = await conn.fetch('''
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'projects'
        ORDER BY ordinal_position
    ''')
    print('Структура таблицы projects:')
    for col in cols:
        null_status = "NULL" if col[2] == "YES" else "NOT NULL"
        print(f'  {col[0]} ({col[1]}) {null_status}')
    await conn.close()

asyncio.run(main())
