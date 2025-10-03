from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database import get_db
import psutil
import os
from datetime import datetime

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    disk_usage = psutil.disk_usage("/")
    disk_free_gb = disk_usage.free / (1024**3)
    disk_status = "healthy" if disk_free_gb > 1.0 else "warning"
    
    memory = psutil.virtual_memory()
    memory_status = "healthy" if memory.percent < 90 else "warning"
    
    overall_status = "healthy" if db_status == "healthy" else "unhealthy"
    
    return {
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": db_status,
            "disk": disk_status,
            "memory": memory_status
        }
    }

@router.get("/ready")
async def readiness_check():
    return {"status": "ready"}

@router.get("/live")
async def liveness_check():
    return {"status": "live"}
