from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Numeric, Text
from src.database import Base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Numeric, Text
from src.database import Base
from sqlalchemy.orm import relationship


class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.cust_id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id"), nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanics.mechanic_id"), nullable=True)
    service_type = Column(String(200), nullable=False)
    complaint = Column(String(200), nullable=True)
    arrival_date = Column(DateTime, nullable=True)
    expected_delivery_date = Column(DateTime, nullable=True)
    labour_charge = Column(Numeric(10, 2), nullable=False, default=0)
    total_service_cost = Column(Numeric(10, 2), nullable=False, default=0)
    additional_notes = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="Pending")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    vehicle = relationship("Vehicle", back_populates="services")
    customer = relationship("Customer", back_populates="services")
    mechanic = relationship("Mechanic", back_populates="services")
    history = relationship("ServiceHistory", back_populates="service", cascade="all, delete-orphan")
    service_parts = relationship("ServicePart", back_populates="service", cascade="all, delete-orphan")


class ServicePart(Base):
    __tablename__ = 'service_parts'

    service_part_id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.service_id'), nullable=False)
    part_id = Column(Integer, ForeignKey('spare_parts.part_id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)

    service = relationship('Service', back_populates='service_parts')
    spare_part = relationship('SparePart', back_populates='service_parts')


class ServiceHistory(Base):
    __tablename__ = "service_history"

    history_id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.service_id"), nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanics.mechanic_id"), nullable=False)
    assigned_at = Column(DateTime, server_default=func.now())

    service = relationship("Service", back_populates="history")
    mechanic = relationship("Mechanic")

    @property
    def service_name(self):
        return self.service.service_type

    @property
    def mechanic_name(self):
        return self.mechanic.mechanic_name