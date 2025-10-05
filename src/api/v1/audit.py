from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.audit_log import AuditLog
from src.schemas.audit_log import AuditLog as AuditLogSchema

router = APIRouter(prefix="/api/v1/audit", tags=["Audit"])

@router.get("/", response_model=list[AuditLogSchema])
def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    logs = db.query(AuditLog)\
              .order_by(AuditLog.timestamp.desc())\
              .offset(skip).limit(limit).all()
    return logs
