from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.customer_management.models import Customer
from src.vehicle_management.models import Vehicle
from src.service_management.models import Service
from src.billing_management.models import Bill
from src.inventory_management.models import SparePart


def get_dashboard_data(db: Session):
    total_customers = db.query(Customer).count()

    total_cars = db.query(Vehicle).filter(func.lower(Vehicle.vehicle_type) == "car").count()

    total_bikes = db.query(Vehicle).filter(func.lower(Vehicle.vehicle_type) == "bike").count()

    vehicles_under_service = db.query(Service).filter(Service.status == "In Progress").count()

    completed_services = db.query(Service).filter(Service.status == "Completed").count()

    pending_services = db.query(Service).filter(Service.status == "Pending").count()

    total_revenue = db.query(func.sum(Bill.paid_amount)).scalar() or Decimal("0.00")

    low_stock_spare_parts = db.query(SparePart).filter(SparePart.available_quantity <= SparePart.minimum_stock_level).count()

    return {
        "total_customers": total_customers,
        "total_cars": total_cars,
        "total_bikes": total_bikes,
        "vehicles_under_service": vehicles_under_service,
        "completed_services": completed_services,
        "pending_services": pending_services,
        "total_revenue": total_revenue,
        "low_stock_spare_parts": low_stock_spare_parts
    }