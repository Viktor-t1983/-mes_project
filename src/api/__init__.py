# API Router imports
from .health import router as health_router
from .day4_endpoints import router as day4_endpoints_router

# Day 4 routers only - others commented to avoid issues
# from .employees import router as employees_router
# from .manufacturing_orders import router as manufacturing_orders_router
# from .operations import router as operations_router
# from .defect_reports import router as defect_reports_router

__all__ = [
    'health_router',
    'day4_endpoints_router'
]
