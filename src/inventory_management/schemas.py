from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional
from decimal import Decimal


class SparePartCreate(BaseModel):
    part_name: str
    part_number: str
    category: Literal["Car", "Bike"]
    available_quantity: int
    price: Decimal
    minimum_stock_level: int


class SparePartUpdate(BaseModel):
    part_name: Optional[str] = None
    part_number: Optional[str] = None
    category: Optional[Literal["Car", "Bike"]] = None
    available_quantity: Optional[int] = None
    price: Optional[Decimal] = None
    minimum_stock_level: Optional[int] = None


class SparePartResponse(BaseModel):
    part_id: int
    part_name: str
    part_number: str
    category: Literal["Car", "Bike"]
    available_quantity: int
    price: Decimal
    minimum_stock_level: int

    model_config = ConfigDict(from_attributes=True)


class SparePartListResponse(BaseModel):
    spare_parts: list[SparePartResponse]


class LowStockResponse(BaseModel):
    message: str
    low_stock_count: int
    spare_parts: list[SparePartResponse]