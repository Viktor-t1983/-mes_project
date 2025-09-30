from .employees import router as employees_router
from .manufacturing_orders import router as manufacturing_orders_router
from .operations import router as operations_router
from .defect_reports import router as defect_reports_router
from .warehouse_items import router as warehouse_items_router
from .incentives import router as incentives_router
from .qr_codes import router as qr_codes_router

__all__ = [
    "employees_router",
    "manufacturing_orders_router",
    "operations_router",
    "defect_reports_router",
    "warehouse_items_router",
    "incentives_router",
    "qr_codes_router"
]
