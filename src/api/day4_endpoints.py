from fastapi import APIRouter, Depends
from src.core.auth import require_role
from src.core.logger import logger

router = APIRouter()

# Day 4 Gamification endpoints
@router.get('/api/v1/achievements')
async def get_achievements(
    current_employee = Depends(require_role("operator"))  # Любой, кто может смотреть
):
    logger.info("Get achievements called", employee_id=current_employee.id)
    return [
        {'id': 1, 'name': 'First Blood', 'description': 'Complete first operation', 'points': 10},
        {'id': 2, 'name': 'Quality Master', 'description': 'Zero defects in shift', 'points': 25},
        {'id': 3, 'name': 'Efficiency Expert', 'description': 'Complete 10 operations in day', 'points': 50}
    ]

@router.post('/api/v1/achievements')
async def create_achievement(
    current_employee = Depends(require_role("admin"))  # Только админ
):
    logger.info("Create achievement called", employee_id=current_employee.id)
    return {'status': 'success', 'message': 'Achievement created'}

@router.get('/api/v1/leaderboard')
async def get_leaderboard(
    current_employee = Depends(require_role("operator"))  # Любой, кто может смотреть
):
    logger.info("Get leaderboard called", employee_id=current_employee.id)
    return [
        {'rank': 1, 'employee_name': 'Ivan Petrov', 'points': 150, 'department': 'Production'},
        {'rank': 2, 'employee_name': 'Maria Ivanova', 'points': 135, 'department': 'Quality'},
        {'rank': 3, 'employee_name': 'Alexey Sidorov', 'points': 135, 'department': 'Logistics'}
    ]

@router.post('/api/v1/1c/sync-invoice')
async def sync_1c_invoice(
    current_employee = Depends(require_role("manager"))  # Только менеджер
):
    logger.info("Sync 1C invoice called", employee_id=current_employee.id)
    return {'status': 'success', 'message': 'Invoice data synchronized with 1C'}
