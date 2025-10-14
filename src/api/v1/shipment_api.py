from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.services.shipment_service import confirm_by_warehouse, confirm_by_transporter
from src.schemas.shipment import ShipmentConfirm, ShipmentTransporterConfirm

router = APIRouter(prefix="/api/v1/shipments", tags=["Day 9 - Shipment"])

@router.post("/{shipment_id}/confirm-warehouse")
async def confirm_warehouse(
    shipment_id: int,
    data: ShipmentConfirm = Body(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        shipment = await confirm_by_warehouse(db, shipment_id, data.employee_qr)
        return {"status": "success", "shipment": shipment}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{shipment_id}/confirm-transporter")
async def confirm_transporter(
    shipment_id: int,
    data: ShipmentTransporterConfirm = Body(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        shipment = await confirm_by_transporter(db, shipment_id, data.transporter_qr, data.tracking_number)
        return {"status": "success", "shipment": shipment}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
