import json
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.operation import Operation
from src.models.offline_buffer import OfflineEvent

async def _sync_start(db: AsyncSession, data):
    # Реализация старта операции (пример)
    op = Operation(
        employee_qr=data.employee_qr,
        part_number=data.part_number,
        workcenter_id=data.workcenter_id,
        status="started"
    )
    db.add(op)
    await db.commit()
    await db.refresh(op)
    return {"status": "started", "operation_id": op.id}

async def _sync_pause(db: AsyncSession, data):
    op = await db.get(Operation, data.operation_id)
    if op and op.status == "started":
        op.status = "paused"
        await db.commit()
        return {"status": "paused", "operation_id": op.id}
    raise ValueError("Operation not found or not started")

async def _sync_complete(db: AsyncSession, data):
    op = await db.get(Operation, data.operation_id)
    if op and op.status in ["started", "paused"]:
        op.status = "completed"
        await db.commit()
        return {"status": "completed", "operation_id": op.id}
    raise ValueError("Operation not found or already completed")

async def _save_to_offline(db: AsyncSession, event_type: str, payload: dict):
    event = OfflineEvent(
        employee_qr=payload.get("employee_qr"),
        event_type=event_type,
        payload=json.dumps(payload)
    )
    db.add(event)
    await db.commit()
    return {"status": "offline_buffered", "event_id": event.id}

async def start_operation(db: AsyncSession, data):
    try:
        return await _sync_start(db, data)
    except Exception:
        return await _save_to_offline(db, "start", data.dict())

async def pause_operation(db: AsyncSession, data):
    try:
        return await _sync_pause(db, data)
    except Exception:
        return await _save_to_offline(db, "pause", data.dict())

async def complete_operation(db: AsyncSession, data):
    try:
        return await _sync_complete(db, data)
    except Exception:
        return await _save_to_offline(db, "complete", data.dict())
