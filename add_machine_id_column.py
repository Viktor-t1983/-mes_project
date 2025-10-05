import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        user='postgres',
        password='MesProject2025',
        database='mes_db',
        host='localhost'
    )
    
    # Проверим, существует ли колонка machine_id
    exists = await conn.fetchval("""
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'operations' AND column_name = 'machine_id'
    """)
    
    if not exists:
        # Добавляем колонку
        await conn.execute("""
            ALTER TABLE operations 
            ADD COLUMN machine_id INTEGER REFERENCES machines(id)
        """)
        print("✅ Колонка machine_id добавлена в таблицу operations")
    else:
        print("ℹ️ Колонка machine_id уже существует")
    
    await conn.close()

asyncio.run(main())
