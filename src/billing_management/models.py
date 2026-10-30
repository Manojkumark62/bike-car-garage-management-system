from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base


class Bill(Base):
    __tablename__ = "bills"

    bill_id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.service_id"), nullable=False, unique=True)
    customer_id = Column(Integer, ForeignKey("customers.cust_id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id"), nullable=False)

    labour_charge = Column(Numeric(10, 2), nullable=False, default=0)
    spare_parts_charge = Column(Numeric(10, 2), nullable=False, default=0)
    tax_amount = Column(Numeric(10, 2), nullable=False, default=0)
    discount_amount = Column(Numeric(10, 2), nullable=False, default=0)
    final_amount = Column(Numeric(10, 2), nullable=False, default=0)

    payment_status = Column(String(20), nullable=False, default="Pending")
    paid_amount = Column(Numeric(10, 2), nullable=False, default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    service = relationship("Service")
    customer = relationship("Customer")
    vehicle = relationship("Vehicle")