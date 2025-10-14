from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func
from src.models.shipment import Shipment
from src.models.employee import Employee
from src.models.project import Project
from src.integrations.one_c_service import OneCIntegrationService
import logging

logger = logging.getLogger(__name__)

async def create_shipment_from_1c(db: AsyncSession,  dict) -> Shipment:
    """Вызывается при синхронизации из 1С"""
    shipment = Shipment(
        project_id=data["project_id"],
        manufacturing_order_id=data["mo_id"],
        invoice_number=data["invoice_number"],
        documents_from_1c=data.get("documents", "")
    )
    db.add(shipment)
    await db.commit()
    await db.refresh(shipment)
    logger.info(f"Shipment {shipment.id} created from 1C invoice {shipment.invoice_number}")
    return shipment

async def confirm_by_warehouse(db: AsyncSession, shipment_id: int, employee_qr: str) -> Shipment:
    from src.services.auth_service import AuthService
    employee = await AuthService.authenticate_by_qr(db, employee_qr)
    shipment = await db.get(Shipment, shipment_id)
    if not shipment:
        raise ValueError("Shipment not found")
    if shipment.status != "created":
        raise ValueError("Shipment already confirmed")
    shipment.status = "ready"
    shipment.confirmed_by_employee_id = employee.id
    await db.commit()
    await db.refresh(shipment)
    logger.info(f"Shipment {shipment_id} confirmed by warehouse")
    return shipment

async def confirm_by_transporter(db: AsyncSession, shipment_id: int, transporter_qr: str, tracking_number: str) -> Shipment:
    from src.services.auth_service import AuthService
    transporter = await AuthService.authenticate_by_qr(db, transporter_qr)
    shipment = await db.get(Shipment, shipment_id)
    if not shipment or shipment.status != "ready":
        raise ValueError("Invalid shipment state")
    shipment.status = "shipped"
    shipment.transporter_qr = transporter_qr
    shipment.tracking_number = tracking_number
    shipment.shipped_at = func.now()
    project = await db.get(Project, shipment.project_id)
    project.status = "completed"
    await db.commit()
    await db.refresh(shipment)
    logger.info(f"Shipment {shipment_id} shipped. Project {shipment.project_id} completed.")
    one_c = OneCIntegrationService()
    await one_c.push_shipment_to_1c({
        "shipment_id": shipment.id,
        "invoice_number": shipment.invoice_number,
        "tracking_number": shipment.tracking_number,
        "shipped_at": shipment.shipped_at.isoformat() if shipment.shipped_at else None,
        "signature": shipment.signature_hash
    })
    return shipment
