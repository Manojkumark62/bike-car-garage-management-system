from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from src.database import Base
from sqlalchemy.orm import relationship


class SparePart(Base):
    __tablename__ = 'spare_parts'

    part_id = Column(Integer, primary_key=True, index=True)
    part_name = Column(String(50), nullable=False)
    part_number = Column(String(50), unique=True, index=True, nullable=False)
    category = Column(String(15), nullable=False)
    available_quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    minimum_stock_level = Column(Integer, nullable=False, default=5)

    service_parts = relationship('ServicePart', back_populates='spare_part')