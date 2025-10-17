import httpx
import logging
from src.core.config import settings

logger = logging.getLogger(__name__)

class PlanFixService:
    """Интеграция с PlanFix: получение сроков проектирования"""
    
    def __init__(self):
        self.base_url = settings.PLANFIX_BASE_URL
        self.api_key = settings.PLANFIX_API_KEY
        self.account = settings.PLANFIX_ACCOUNT

    async def get_project_deadline(self, project_id: str) -> dict:
        """Получить срок завершения проектирования из PlanFix"""
        if not self.base_url or not self.api_key:
            logger.warning("PlanFix integration disabled")
            return {"status": "fallback", "deadline_days": 3}  # fallback: 3 дня
        
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    f"{self.base_url}/task/get",
                    json={
                        "account": self.account,
                        "apiKey": self.api_key,
                        "taskId": project_id
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    # Пример: извлекаем дедлайн из custom fields
                    deadline = data.get("customFields", {}).get("deadline", None)
                    return {"status": "success", "deadline": deadline}
                else:
                    logger.error(f"PlanFix error: {response.status_code}")
                    return {"status": "error", "fallback_days": 3}
        except Exception as e:
            logger.exception("PlanFix connection failed")
            return {"status": "error", "fallback_days": 3}
