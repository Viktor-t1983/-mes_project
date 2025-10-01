import qrcode
from io import BytesIO
from fastapi.responses import Response

def generate_qr_code(data: str) -> Response:
    """Генерирует QR код и возвращает его как изображение PNG"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Сохраняем изображение в буфер
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    # Возвращаем изображение как ответ
    return Response(content=img_buffer.getvalue(), media_type="image/png")
