from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.services.operation_service import start_operation, pause_operation, complete_operation
from src.schemas.operation import OperationStart, OperationPause, OperationComplete

router = APIRouter(prefix="/mobile", tags=["Day 11 - Mobile"])

@router.post("/operations/start")
async def mobile_start_op(data: OperationStart, db: AsyncSession = Depends(get_db)):
    return await start_operation(db, data)

@router.post("/operations/pause")
async def mobile_pause_op(data: OperationPause, db: AsyncSession = Depends(get_db)):
    return await pause_operation(db, data)

@router.post("/operations/complete")
async def mobile_complete_op(data: OperationComplete, db: AsyncSession = Depends(get_db)):
    return await complete_operation(db, data)
