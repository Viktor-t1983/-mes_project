from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models.meta_process import MetaProcess, MetaStep
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

router = APIRouter(prefix="/api/v1/meta", tags=["Meta BPM"])

class MetaStepCreate(BaseModel):
    step_order: int
    name: str
    action_type: str
    config: Dict[str, Any] = Field(default_factory=dict)  # ← Ключевое исправление

class MetaProcessCreate(BaseModel):
    name: str
    description: Optional[str] = None
    steps: List[MetaStepCreate]

@router.post("/processes", status_code=status.HTTP_201_CREATED)
async def create_process(process: MetaProcessCreate, db: AsyncSession = Depends(get_db)):
    db_process = MetaProcess(name=process.name, description=process.description)
    db.add(db_process)
    await db.flush()
    for step in process.steps:
        db_step = MetaStep(
            process_id=db_process.id,
            step_order=step.step_order,
            name=step.name,
            action_type=step.action_type,
            config=step.config
        )
        db.add(db_step)
    await db.commit()
    await db.refresh(db_process)
    return {"id": db_process.id, "name": db_process.name}

@router.get("/processes")
async def list_processes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(MetaProcess.__table__.select())
    return result.fetchall()
