from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.models.defect_report import DefectReport
from src.schemas.defect_report import DefectReportCreate, DefectReportCreate

def get_defect_report(db: Session, defect_id: int):
    return db.query(DefectReport).filter(DefectReport.id == defect_id).first()

def get_defect_reports(db: Session, skip: int = 0, limit: int = 100, status: str = None, severity: str = None):
    query = db.query(DefectReport)
    if status:
        query = query.filter(DefectReport.status == status)
    if severity:
        query = query.filter(DefectReport.severity == severity)
    return query.offset(skip).limit(limit).all()

def get_defect_reports_by_order(db: Session, manufacturing_order_id: int, skip: int = 0, limit: int = 100):
    return db.query(DefectReport).filter(
        DefectReport.manufacturing_order_id == manufacturing_order_id
    ).offset(skip).limit(limit).all()

def create_defect_report(db: Session, defect_report: DefectReportCreate):
    db_defect = DefectReport(
        manufacturing_order_id=defect_report.manufacturing_order_id,
        operation_id=defect_report.operation_id,
        reported_by=defect_report.reported_by,
        defect_type=defect_report.defect_type,
        defect_description=defect_report.defect_description,
        severity=defect_report.severity,
        quantity_affected=defect_report.quantity_affected,
        corrective_action=defect_report.corrective_action,
        status=defect_report.status
    )
    db.add(db_defect)
    db.commit()
    db.refresh(db_defect)
    return db_defect

def update_defect_report(db: Session, defect_id: int, defect_report: DefectReportCreate):
    db_defect = db.query(DefectReport).filter(DefectReport.id == defect_id).first()
    if db_defect:
        update_data = defect_report.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_defect, field, value)
        db.commit()
        db.refresh(db_defect)
    return db_defect

def resolve_defect_report(db: Session, defect_id: int, resolved_by: int, corrective_action: str = None):
    db_defect = db.query(DefectReport).filter(DefectReport.id == defect_id).first()
    if db_defect:
        db_defect.status = "resolved"
        db_defect.resolved_by = resolved_by
        from datetime import datetime
        db_defect.resolved_at = datetime.now()
        if corrective_action:
            db_defect.corrective_action = corrective_action
        db.commit()
        db.refresh(db_defect)
    return db_defect
