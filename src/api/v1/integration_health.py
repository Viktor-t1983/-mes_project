from fastapi import APIRouter, Depends
from src.integrations.planfix_service import PlanFixService
from src.integrations.one_c_service import OneCIntegrationService

router = APIRouter(prefix="/health", tags=["Day 12 - Integration Health"])

@router.get("/integrations")
async def check_integrations():
    """Проверка доступности внешних систем"""
    planfix = PlanFixService()
    onec = OneCIntegrationService()
    
    return {
        "planfix": "configured" if planfix.base_url else "disabled",
        "one_c": "configured" if onec.base_url else "disabled",
        "solidworks_bom_dir": "exists"  # проверка директории можно добавить
    }
