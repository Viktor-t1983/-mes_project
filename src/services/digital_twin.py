from sqlalchemy.orm import Session
from src.models.operation import Operation
from datetime import datetime, timedelta

def calculate_oee(db: Session, machine_id: int) -> dict:
    """Рассчитывает OEE для станка за последние 24 часа"""
    now = datetime.utcnow()
    start = now - timedelta(hours=24)

    available_time = 24 * 60  # минут

    downtime = db.query(Operation.pause_duration)\
                  .filter(Operation.machine_id == machine_id,
                          Operation.planned_start >= start)\
                  .scalar() or 0

    operating_time = available_time - downtime

    completed_ops = db.query(Operation.id)\
                      .filter(Operation.machine_id == machine_id,
                              Operation.planned_start >= start,
                              Operation.status == "completed")\
                      .count()
    ideal_time = completed_ops * 10  # 10 мин на операцию

    availability = operating_time / available_time if available_time > 0 else 0
    performance = ideal_time / operating_time if operating_time > 0 else 0
    quality = 0.95

    oee = availability * performance * quality

    return {
        "oee": round(oee * 100, 2),
        "availability": round(availability * 100, 2),
        "performance": round(performance * 100, 2),
        "quality": round(quality * 100, 2),
        "downtime_minutes": downtime,
        "completed_operations": completed_ops
    }
