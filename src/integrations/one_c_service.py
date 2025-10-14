import httpx
import logging
from src.core.config import settings

logger = logging.getLogger(__name__)

class OneCIntegrationService:
    def __init__(self):
        self.base_url = settings.ONE_C_BASE_URL or None
        self.auth = (
            settings.ONE_C_USERNAME or "",
            settings.ONE_C_PASSWORD or ""
        )

    async def push_shipment_to_1c(self, shipment: dict) -> bool:
        if not self.base_url:
            logger.warning("1C integration disabled: ONE_C_BASE_URL not set")
            return True

        try:
            async with httpx.AsyncClient(auth=self.auth, timeout=10.0) as client:
                url = f"{self.base_url}/api/v1/shipments"
                response = await client.post(
                    url,
                    json=shipment,
                    headers={"Content-Type": "application/json"}
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"1C shipment sync failed: {e}")
            return False
