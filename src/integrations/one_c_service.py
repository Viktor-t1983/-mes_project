import httpx
import logging
from src.core.config import settings

logger = logging.getLogger(__name__)

class OneCIntegrationService:
    def __init__(self):
        self.base_url = settings.ONE_C_BASE_URL
        self.auth = (
            settings.ONE_C_USER,        # ← Используем ONE_C_USER
            settings.ONE_C_PASSWORD
        )

    async def push_shipment_to_1c(self, shipment_data: dict) -> bool:
        if not self.base_url:
            logger.warning("1C integration disabled")
            return True  # считаем успешным, если не настроено

        try:
            async with httpx.AsyncClient(auth=self.auth, timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/shipments",
                    json=shipment_data,
                    headers={"Content-Type": "application/json"}
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"1C shipment sync failed: {e}")
            return False
