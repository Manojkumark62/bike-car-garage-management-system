from pydantic import BaseModel
from decimal import Decimal


class DashboardResponse(BaseModel):
    total_customers: int
    total_cars: int
    total_bikes: int
    vehicles_under_service: int
    completed_services: int
    pending_services: int
    total_revenue: Decimal
    low_stock_spare_parts: int