import aiohttp
import logging
logger = logging.getLogger(__name__)

class OneCService:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    async def sync_invoice(self, invoice_data: dict):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/v1/sync/invoice",
                    json=invoice_data
                ) as response:
                    if response.status == 200:
                        return {"status": "success", "message": "Invoice synced"}
                    else:
                        return {"status": "error", "message": f"1C error: {response.status}"}
        except Exception as e:
            return {"status": "error", "message": f"Network error: {e}"}
