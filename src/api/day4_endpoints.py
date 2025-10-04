from fastapi import APIRouter
from src.core.logger import logger

router = APIRouter()

# Day 4 Gamification endpoints
@router.get('/api/v1/achievements')
async def get_achievements():
    logger.info("Get achievements called")
    return [
        {'id': 1, 'name': 'First Blood', 'description': 'Complete first operation', 'points': 10},
        {'id': 2, 'name': 'Quality Master', 'description': 'Zero defects in shift', 'points': 25},
        {'id': 3, 'name': 'Efficiency Expert', 'description': 'Complete 10 operations in day', 'points': 50}
    ]

@router.post('/api/v1/achievements')
async def create_achievement():
    logger.info("Create achievement called")
    return {'status': 'success', 'message': 'Achievement created'}

@router.get('/api/v1/leaderboard')
async def get_leaderboard():
    logger.info("Get leaderboard called")
    return [
        {'rank': 1, 'employee_name': 'Ivan Petrov', 'points': 150, 'department': 'Production'},
        {'rank': 2, 'employee_name': 'Maria Ivanova', 'points': 135, 'department': 'Quality'},
        {'rank': 3, 'employee_name': 'Alexey Sidorov', 'points': 135, 'department': 'Logistics'}
    ]

@router.post('/api/v1/1c/sync-invoice')
async def sync_1c_invoice():
    logger.info("Sync 1C invoice called")
    return {'status': 'success', 'message': 'Invoice data synchronized with 1C'}
