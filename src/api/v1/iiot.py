from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.core.database import get_db
from src.models.machine import Machine

router = APIRouter(prefix="/api/v1/iiot", tags=["IIoT"])

@router.post("/heartbeat")
async def machine_heartbeat(
    event_type: str,
    machine_token: str = Header(..., alias="X-Machine-Token"),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Machine).where(Machine.machine_token == machine_token))
    machine = result.scalar_one_or_none()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    # Логика heartbeat
    return {"status": "ok", "machine_id": machine.id}
