import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.core.database import get_db
from src.integrations import OneCIntegrationService

async def retry_sync_queue():
    """Фоновая задача: повторная отправка в 1С каждые 30 секунд"""
    while True:
        await asyncio.sleep(30)
        async for db in get_db():
            try:
                # Используем text() для сырого SQL
                result = await db.execute(
                    text("SELECT * FROM sync_queue WHERE is_synced = false AND error_count < 5")
                )
                rows = result.fetchall()
                for row in rows:
                    try:
                        payload = json.loads(row.payload)
                        success = await OneCIntegrationService().push_invoice_to_1c(payload)
                        if success:
                            await db.execute(
                                text("UPDATE sync_queue SET is_synced = true WHERE id = :id"),
                                {"id": row.id}
                            )
                        else:
                            await db.execute(
                                text("UPDATE sync_queue SET error_count = error_count + 1 WHERE id = :id"),
                                {"id": row.id}
                            )
                        await db.commit()
                    except Exception as e:
                        await db.execute(
                            text("UPDATE sync_queue SET last_error = :err WHERE id = :id"),
                            {"id": row.id, "err": str(e)}
                        )
                        await db.commit()
            except Exception as e:
                # Логируем, но не падаем
                print(f"⚠️ Sync worker error: {e}")
