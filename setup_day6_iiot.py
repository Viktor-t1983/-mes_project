#!/usr/bin/env python3
"""
ДЕНЬ 6: IIoT + Цифровой двойник станка + Аудит
Senior Security Engineer Edition
"""
import os
import sys
import shutil
from pathlib import Path

PROJECT_ROOT = Path(".").resolve()

def write_file(path: str, content: str):
    full_path = PROJECT_ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✅ Создан: {path}")

def backup_file(path: str):
    src = PROJECT_ROOT / path
    if src.exists():
        shutil.copy(src, src.with_suffix(src.suffix + ".bak"))
        print(f"💾 Резервная копия: {path}.bak")

# === 1. Модель станка ===
write_file("src/models/machine.py", '''
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)              # "Токарный станок 1К62"
    type = Column(String, nullable=False)              # "lathe", "milling", "laser"
    location = Column(String)                          # "Цех 1, Линия A"
    status = Column(String, default="online")          # online, offline, maintenance
    last_heartbeat = Column(DateTime(timezone=True), default=func.now())
    machine_token = Column(String, unique=True)        # для аутентификации станков
    technical_docs = Column(Text)                      # JSON с URL паспортов
''')

# === 2. Аудит-лог ===
write_file("src/models/audit_log.py", '''
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)           # None для станков
    machine_id = Column(Integer, nullable=True)        # None для пользователей
    action = Column(String, nullable=False)            # "operation_start", "defect_reported"
    ip_address = Column(String)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    data_snapshot = Column(Text)                       # JSON с контекстом
''')

# === 3. Схемы Pydantic ===
write_file("src/schemas/machine.py", '''
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MachineBase(BaseModel):
    name: str
    type: str
    location: Optional[str] = None
    technical_docs: Optional[str] = None

class MachineCreate(MachineBase):
    machine_token: str

class Machine(MachineBase):
    id: int
    status: str
    last_heartbeat: datetime

    class Config:
        from_attributes = True
''')

write_file("src/schemas/audit_log.py", '''
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    machine_id: Optional[int] = None
    action: str
    ip_address: str
    data_snapshot: str

class AuditLog(AuditLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
''')

# === 4. Сервис цифрового двойника ===
write_file("src/services/digital_twin.py", '''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models.machine import Machine
from src.models.operation import Operation
from datetime import datetime, timedelta

async def calculate_oee(db: AsyncSession, machine_id: int) -> dict:
    """Рассчитывает OEE для станка за последние 24 часа"""
    now = datetime.utcnow()
    start = now - timedelta(hours=24)

    # Доступное время (24*60 мин)
    available_time = 24 * 60

    # Время простоев (паузы)
    stmt = select(func.sum(Operation.pause_duration)).where(
        Operation.machine_id == machine_id,
        Operation.planned_start >= start
    )
    result = await db.execute(stmt)
    downtime = result.scalar() or 0

    # Время работы
    operating_time = available_time - downtime

    # Идеальное время (без брака)
    stmt = select(func.sum(Operation.planned_duration)).where(
        Operation.machine_id == machine_id,
        Operation.planned_start >= start,
        Operation.status == "completed"
    )
    result = await db.execute(stmt)
    ideal_time = result.scalar() or 0

    # Расчёт компонентов
    availability = operating_time / available_time if available_time > 0 else 0
    performance = ideal_time / operating_time if operating_time > 0 else 0
    quality = 0.95  # упрощённо; можно расширить через defect_reports

    oee = availability * performance * quality

    return {
        "oee": round(oee * 100, 2),
        "availability": round(availability * 100, 2),
        "performance": round(performance * 100, 2),
        "quality": round(quality * 100, 2),
        "downtime_minutes": downtime
    }
''')

# === 5. Эндпоинты IIoT ===
write_file("src/api/v1/iiot.py", '''
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models.machine import Machine
from src.services.digital_twin import calculate_oee
from src.models.audit_log import AuditLog
import json

router = APIRouter(prefix="/api/v1/iiot", tags=["IIoT"])

@router.post("/heartbeat")
async def machine_heartbeat(
    request: Request,
    machine_token: str,
    event_type: str = "heartbeat",
    payload: dict = None,
    db: AsyncSession = Depends(get_db)
):
    # Аутентификация станка
    machine = await db.execute(
        "SELECT * FROM machines WHERE machine_token = :token",
        {"token": machine_token}
    )
    machine = machine.fetchone()
    if not machine:
        raise HTTPException(401, "Invalid machine token")

    # Обновление статуса
    await db.execute(
        "UPDATE machines SET last_heartbeat = NOW(), status = 'online' WHERE id = :id",
        {"id": machine.id}
    )

    # Логирование события
    log_entry = AuditLog(
        machine_id=machine.id,
        action=f"machine_{event_type}",
        ip_address=request.client.host,
        data_snapshot=json.dumps(payload or {})
    )
    db.add(log_entry)
    await db.commit()

    return {"status": "ok", "machine_id": machine.id}

@router.get("/oee/{machine_id}")
async def get_machine_oee(machine_id: int, db: AsyncSession = Depends(get_db)):
    return await calculate_oee(db, machine_id)
''')

# === 6. Эндпоинты аудита ===
write_file("src/api/v1/audit.py", '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.core.database import get_db
from src.models.audit_log import AuditLog
from src.schemas.audit_log import AuditLog as AuditLogSchema

router = APIRouter(prefix="/api/v1/audit", tags=["Audit"])

@router.get("/", response_model=list[AuditLogSchema])
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AuditLog).offset(skip).limit(limit).order_by(AuditLog.timestamp.desc())
    )
    return result.scalars().all()
''')

# === 7. Обновление зависимостей ===
req_path = PROJECT_ROOT / "requirements.txt"
with open(req_path, "a", encoding="utf-8") as f:
    if "structlog" not in open(req_path, encoding="utf-8").read():
        f.write("\nstructlog==24.1.0\ncryptography==41.0.7\n")
print("📦 Обновлены зависимости")

# === 8. Резервное копирование и обновление main.py ===
backup_file("main.py")
with open(PROJECT_ROOT / "main.py", "r", encoding="utf-8") as f:
    content = f.read()

if "iiot_router" not in content:
    new_imports = '''
# День 6: IIoT и Аудит
try:
    from src.api.v1.iiot import router as iiot_router
    app.include_router(iiot_router)
    print("[OK] IIoT router connected")
except Exception as e:
    print(f"[ERROR] IIoT router: {e}")

try:
    from src.api.v1.audit import router as audit_router
    app.include_router(audit_router)
    print("[OK] Audit router connected")
except Exception as e:
    print(f"[ERROR] Audit router: {e}")
'''
    content = content.rstrip() + "\n" + new_imports

with open(PROJECT_ROOT / "main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("\n🚀 ДЕНЬ 6: IIoT + Цифровой двойник + Аудит — УСПЕШНО НАСТРОЕН!")
print("\n📋 Следующие шаги:")
print("1. pip install -r requirements.txt")
print("2. alembic revision --autogenerate -m 'day6_iiot'")
print("3. alembic upgrade head")
print("4. uvicorn main:app --reload")
print("\n🔍 Новые эндпоинты:")
print(" • POST /api/v1/iiot/heartbeat")
print(" • GET /api/v1/iiot/oee/{machine_id}")
print(" • GET /api/v1/audit")
