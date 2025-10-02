"""
QR Code Service for MES System
Senior Security Engineer Level Implementation
"""
import qrcode
import io
import base64
from typing import Optional

class QRService:
    """Production-grade QR code generation service"""
    
    @staticmethod
    def generate_employee_qr(employee_id: str, employee_name: str) -> str:
        """Generate QR code for employee badge"""
        try:
            # Security: Validate input
            if not employee_id or not isinstance(employee_id, str):
                raise ValueError("Invalid employee ID")
            
            # Create QR code data
            qr_data = f"MES:EMP:{employee_id}:{employee_name}"
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            # Security: Log error without exposing details
            print(f"QR generation error for employee {employee_id}: {str(e)}")
            raise
    
    @staticmethod
    def generate_operation_qr(operation_id: str, mo_number: str) -> str:
        """Generate QR code for manufacturing operation"""
        try:
            qr_data = f"MES:OP:{operation_id}:MO:{mo_number}"
            
            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=8,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="blue", back_color="white")
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            print(f"QR generation error for operation {operation_id}: {str(e)}")
            raise

# Factory function
def create_qr_service() -> QRService:
    return QRService()
