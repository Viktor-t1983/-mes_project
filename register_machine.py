import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        user='postgres',
        password='MesProject2025',
        database='mes_db',
        host='localhost'
    )
    await conn.execute("""
        INSERT INTO machines (name, type, machine_token, location)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (machine_token) DO NOTHING
    """, "Тестовый станок", "test", "test_token", "Цех 1")
    print("✅ Станок зарегистрирован")
    await conn.close()

asyncio.run(main())
