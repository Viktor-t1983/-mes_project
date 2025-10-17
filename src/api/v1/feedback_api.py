from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.core.logging import logger

router = APIRouter(prefix="/api/v1/feedback", tags=["Day 10 - Feedback"])

@router.post("/")
async def submit_feedback(
    feedback: dict = Body(...),
    db: AsyncSession = Depends(get_db)
):
    logger.info("feedback_submitted", **feedback)
    return {"status": "received", "message": "Спасибо за обратную связь!"}
