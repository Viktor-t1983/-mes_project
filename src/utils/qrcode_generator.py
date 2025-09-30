import qrcode
from PIL import Image
import io

def generate_qr_code(data: str) -> bytes:
    """
    Генерирует QR-код из строки данных
    Возвращает bytes изображения PNG
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# Тестовая функция для проверки
def test_qr():
    return "QR generator is working!"