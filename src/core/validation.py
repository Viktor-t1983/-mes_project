from pydantic import BaseModel, field_validator
from typing import Optional

class QRCodeValidator(BaseModel):
    qr_code: str

    @field_validator('qr_code')
    def validate_qr_code(cls, v):
        if not v or len(v) < 5:
            raise ValueError('QR-код должен быть не короче 5 символов')
        if ';' in v or '--' in v or 'DROP' in v.upper():
            raise ValueError('Запрещённые символы в QR-коде')
        return v
