from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.machine import Machine
from src.models.audit_log import AuditLog
from src.services.digital_twin import calculate_oee
import json

router = APIRouter(prefix="/api/v1/iiot", tags=["IIoT"])

@router.post("/heartbeat")
def machine_heartbeat(
    request: Request,
    machine_token: str = Header(..., alias="X-Machine-Token"),
    event_type: str = "heartbeat",
    payload: dict = None,
    db: Session = Depends(get_db)
):
    # Аутентификация станка
    machine = db.query(Machine).filter(Machine.machine_token == machine_token).first()
    if not machine:
        raise HTTPException(401, "Invalid machine token")

    # Обновление статуса
    machine.status = "online"
    db.add(machine)

    # Логирование события
    log_entry = AuditLog(
        machine_id=machine.id,
        action=f"machine_{event_type}",
        ip_address=request.client.host,
        data_snapshot=json.dumps(payload or {})
    )
    db.add(log_entry)
    db.commit()

    return {"status": "ok", "machine_id": machine.id}

@router.get("/oee/{machine_id}")
def get_machine_oee(machine_id: int, db: Session = Depends(get_db)):
    return calculate_oee(db, machine_id)
