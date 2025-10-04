import httpx
import os
from typing import Dict, Any

class OneCIntegrationService:
    def __init__(self):
        self.base_url = os.getenv("ONE_C_BASE_URL", "http://1c.yourcompany.local")
        self.auth = (
            os.getenv("ONE_C_USERNAME", "mes_user"),
            os.getenv("ONE_C_PASSWORD", "secure_password")
        )
        self.timeout = 30.0
    
    async def push_invoice_to_1c(self, invoice_ Dict[str, Any]) -> bool:
        try:
            async with httpx.AsyncClient(auth=self.auth, timeout=self.timeout) as client:
                response = await client.post(f"{self.base_url}/api/v1/invoices", json=invoice_data)
                return response.status_code == 200
        except Exception as e:
            print(f"❌ Ошибка 1С: {e}")
            return False
