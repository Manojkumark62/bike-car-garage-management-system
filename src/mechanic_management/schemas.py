from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class MechanicCreate(BaseModel):
    mechanic_name : str
    contact_number: str = Field(min_length=10, max_length=10)
    specialization : str
    experience : int

class MechanicUpdate(BaseModel):
    mechanic_name : str | None = None
    contact_number: str = Field(min_length=10, max_length=10)
    specialization : str | None = None
    experience : int | None = None

class MechanicResponse(BaseModel):
    mechanic_id : int
    mechanic_name : str
    contact_number : int
    specialization : str
    experience : int
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True)