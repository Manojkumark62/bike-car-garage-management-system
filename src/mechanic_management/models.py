from sqlalchemy import Column, Integer, String, func, DateTime
from sqlalchemy.orm import relationship
from src.database import Base

class Mechanic(Base):
    __tablename__ = 'mechanics'
    mechanic_id = Column(Integer, primary_key = True, index = True)
    mechanic_name = Column(String(100), nullable = False)
    contact_number = Column(String(20),unique = True, nullable = False)
    specialization = Column(String(100), nullable = False)
    experience = Column(Integer, nullable = False)
    created_at = Column(DateTime, server_default = func.now())
    updated_at = Column(DateTime, server_default = func.now(), onupdate = func.now())

    services = relationship('Service', back_populates = 'mechanic')