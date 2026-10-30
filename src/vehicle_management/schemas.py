from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional
from datetime import datetime

class CreateVehicleRequest(BaseModel):
    customer_id: int
    registration_number: str
    vehicle_type: Literal["Car", "Bike"]
    brand: str
    model: str
    fuel_type: str

class UpdateVehicleRequest(BaseModel):
    customer_id: Optional[int] = None
    registration_number: Optional[str] = None
    vehicle_type: Optional[Literal["Car", "Bike"]] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    fuel_type: Optional[Literal["Petrol", "Diesel", "Electric", "CNG"]] = None

class VehicleResponse(BaseModel):
    vehicle_id: int
    customer_id: int
    registration_number: str
    vehicle_type: Literal["Car", "Bike"]
    brand: str
    model: str
    fuel_type: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class VehicleListResponse(BaseModel):
    vehicles: list[VehicleResponse]