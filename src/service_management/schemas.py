from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from datetime import datetime

class ServiceCreate(BaseModel):
    customer_id: int
    vehicle_id: int
    mechanic_id: int
    service_type: str = Field(..., min_length=1, max_length=100)
    complaint: str | None = Field(None, max_length=500)
    arrival_date: datetime | None = None
    labour_charge: float = Field(..., ge=0)
    total_service_cost: float = Field(..., ge=0)
    additional_notes: str | None = Field(None, max_length=1000)
    expected_delivery_date: datetime | None = None


class ServiceUpdate(BaseModel):
    customer_id: int | None = None
    vehicle_id: int | None = None
    mechanic_id: int| None = None
    service_type: str | None = Field(None, min_length=1, max_length=100)
    complaint: str | None = Field(None, max_length=500)
    arrival_date: datetime | None = None
    labour_charge: float | None = Field(None, ge=0)
    total_service_cost: float | None = Field(None, ge=0)
    additional_notes: str | None = Field(None, max_length=1000)
    expected_delivery_date: datetime | None = None


class ServiceResponse(BaseModel):
    service_id: int
    customer_id: int
    vehicle_id: int
    mechanic_id: int
    service_type: str
    complaint: str | None = None
    arrival_date: datetime | None = None
    labour_charge: float
    total_service_cost: float
    additional_notes: str | None = None
    expected_delivery_date: datetime | None = None
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ServicePartCreate(BaseModel):
    part_id: int
    quantity: int = Field(..., gt=0)


class ServicePartResponse(BaseModel):
    service_part_id: int
    service_id: int
    part_id: int
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class ServicePartListResponse(BaseModel):
    service_parts: list[ServicePartResponse]


class ServiceHistoryResponse(BaseModel):
    history_id: int
    service_name: str
    mechanic_name: str
    assigned_at: datetime

    model_config = ConfigDict(from_attributes=True)