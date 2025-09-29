from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.core.database import get_db
from src.schemas.defect_report import DefectReport, DefectReportCreate, DefectReportUpdate
from src.crud.defect_report import (
    get_defect_report, get_defect_reports, get_defect_reports_by_order,
    create_defect_report, update_defect_report, resolve_defect_report
)

router = APIRouter(prefix="/defect-reports", tags=["defect-reports"])

@router.get("/", response_model=List[DefectReport])
def read_defect_reports(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter by status"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    db: Session = Depends(get_db)
):
    reports = get_defect_reports(db, skip=skip, limit=limit, status=status, severity=severity)
    return reports

@router.get("/{defect_id}", response_model=DefectReport)
def read_defect_report(defect_id: int, db: Session = Depends(get_db)):
    db_defect = get_defect_report(db, defect_id=defect_id)
    if db_defect is None:
        raise HTTPException(status_code=404, detail="Defect report not found")
    return db_defect

@router.get("/order/{order_id}", response_model=List[DefectReport])
def read_defect_reports_by_order(order_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reports = get_defect_reports_by_order(db, manufacturing_order_id=order_id, skip=skip, limit=limit)
    return reports

@router.post("/", response_model=DefectReport, status_code=status.HTTP_201_CREATED)
def create_new_defect_report(report: DefectReportCreate, db: Session = Depends(get_db)):
    return create_defect_report(db=db, defect_report=report)

@router.put("/{defect_id}", response_model=DefectReport)
def update_existing_defect_report(defect_id: int, report: DefectReportUpdate, db: Session = Depends(get_db)):
    db_defect = update_defect_report(db, defect_id=defect_id, defect_report=report)
    if db_defect is None:
        raise HTTPException(status_code=404, detail="Defect report not found")
    return db_defect

@router.post("/{defect_id}/resolve", response_model=DefectReport)
def resolve_defect_report_endpoint(
    defect_id: int, 
    resolved_by: int,
    corrective_action: Optional[str] = None,
    db: Session = Depends(get_db)
):
    db_defect = resolve_defect_report(db, defect_id=defect_id, resolved_by=resolved_by, corrective_action=corrective_action)
    if db_defect is None:
        raise HTTPException(status_code=404, detail="Defect report not found")
    return db_defect
