from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base

class Vehicle(Base):
    __tablename__ = 'vehicles'
    vehicle_id = Column(Integer, primary_key = True, index = True)
    customer_id = Column(Integer, ForeignKey("customers.cust_id"), nullable=False)
    vehicle_type = Column(String(50), nullable = False)
    brand = Column(String(100), nullable = False)
    registration_number = Column(String(20), unique=True, nullable=False, index=True)
    model = Column(String(100), nullable = False)
    fuel_type = Column(String(50), nullable = False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="vehicles")
    services = relationship ("Service", back_populates="vehicle")