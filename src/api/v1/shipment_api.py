from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models.shipment import Shipment as ShipmentModel
from src.schemas.shipment import ShipmentCreate, ShipmentResponse, ShipmentConfirm, ShipmentTransporterConfirm
from src.services.shipment_service import confirm_by_warehouse, confirm_by_transporter

router = APIRouter(prefix="/api/v1/shipments", tags=["Day 13 - E2E"])

@router.post("/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(shipment: ShipmentCreate, db: AsyncSession = Depends(get_db)):
    signature = ShipmentModel.generate_signature(
        shipment.project_id,
        shipment.manufacturing_order_id,
        shipment.invoice_number
    )
    db_shipment = ShipmentModel(
        **shipment.dict(),
        signature_hash=signature
    )
    db.add(db_shipment)
    await db.commit()
    await db.refresh(db_shipment)
    return db_shipment

@router.post("/{shipment_id}/confirm-warehouse")
async def confirm_warehouse(shipment_id: int, data: ShipmentConfirm, db: AsyncSession = Depends(get_db)):
    try:
        shipment = await confirm_by_warehouse(db, shipment_id, data.employee_qr)
        return {"status": "success", "shipment": shipment}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{shipment_id}/confirm-transporter")
async def confirm_transporter(shipment_id: int, data: ShipmentTransporterConfirm, db: AsyncSession = Depends(get_db)):
    try:
        shipment = await confirm_by_transporter(db, shipment_id, data.transporter_qr, data.tracking_number)
        return {"status": "success", "shipment": shipment}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
