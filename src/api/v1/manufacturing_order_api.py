from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models.manufacturing_order import ManufacturingOrder as MOModel
from src.schemas.manufacturing_order import ManufacturingOrderCreate, ManufacturingOrderResponse

router = APIRouter(prefix="/api/v1/manufacturing-orders", tags=["Manufacturing Orders"])

@router.post("/", response_model=ManufacturingOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_manufacturing_order(mo: ManufacturingOrderCreate, db: AsyncSession = Depends(get_db)):
    db_mo = MOModel(**mo.dict())
    db.add(db_mo)
    await db.commit()
    await db.refresh(db_mo)
    return db_mo
