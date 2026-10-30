from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base

class Customer(Base):
    __tablename__ = 'customers'

    cust_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    address = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    vehicles = relationship("Vehicle", back_populates="customer")
    services = relationship("Service", back_populates="customer")