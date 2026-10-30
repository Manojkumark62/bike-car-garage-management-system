from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class CreateCustomerRequest(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    address: str

class UpdateCustomerRequest(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    address: str

class CustomerResponse(BaseModel):
    cust_id: int
    name: str
    email: EmailStr
    phone_number: str
    address: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CustomerListResponse(BaseModel):
    customers: list[CustomerResponse]
    