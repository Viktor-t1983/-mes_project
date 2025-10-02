from .base import Base
from .gamification import Achievement, EmployeeAchievement, Leaderboard

# Импорты для существующих моделей (если есть)
try:
    from .employee import Employee
    from .operation import Operation
    from .manufacturing_order import ManufacturingOrder
    from .warehouse_item import WarehouseItem
    from .defect_report import DefectReport
    from .incentive import Incentive
except ImportError:
    pass

__all__ = [
    'Base',
    'Achievement',
    'EmployeeAchievement', 
    'Leaderboard'
]
