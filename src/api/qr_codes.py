from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from src.core.database import get_db
import src.utils.qrcode_generator as qr_gen
from src.crud.manufacturing_order import get_manufacturing_order
import json

router = APIRouter()

@router.get("/qr/order/{order_id}")
def generate_order_qr(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Сгенерировать QR-код для производственного заказа.
    """
    # Получаем заказ
    order = get_manufacturing_order(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Создаем данные для QR
    qr_data = {
        "type": "manufacturing_order",
        "order_id": order.id,
        "order_number": order.order_number,
        "product_name": order.product_name,
        "quantity": order.quantity,
        "status": order.status
    }
    
    # Генерируем QR-код
    qr_image = qr_gen.generate_qr_code(json.dumps(qr_data))
    
    # Возвращаем изображение
    return Response(content=qr_image, media_type="image/png")
