import asyncio
import asyncpg
import hashlib
from datetime import datetime

def generate_signature(project_id: int, invoice_number: str) -> str:
    payload = f"{project_id}:{invoice_number}:created:{datetime.utcnow().isoformat()}"
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

async def main():
    conn = await asyncpg.connect(
        user='postgres',
        password='MesProject2025',
        database='mes_db',
        host='localhost'
    )

    # Убедимся, что MO 999 существует
    mo_exists = await conn.fetchval("SELECT 1 FROM manufacturing_orders WHERE id = 999")
    if not mo_exists:
        raise RuntimeError("Manufacturing Order with id=999 does not exist")

    sig_hash = generate_signature(4, 'INV-999')

    # Выполняем INSERT без переносов в строке
    query = """
    INSERT INTO shipments (id, project_id, manufacturing_order_id, invoice_number, status, signature_hash)
    VALUES ($1, $2, $3, $4, $5, $6)
    ON CONFLICT (id) DO NOTHING
    """
    await conn.execute(query, 999, 4, 999, 'INV-999', 'created', sig_hash)
    print('✅ Отгрузка id=999 создана со статусом "created"')
    await conn.close()

asyncio.run(main())
