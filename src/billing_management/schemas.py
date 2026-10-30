from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime


class BillCreate(BaseModel):
    service_id: int
    tax_amount: Decimal = Field(default=0, ge=0)
    discount_amount: Decimal = Field(default=0, ge=0)


class PaymentUpdate(BaseModel):
    paid_amount: Decimal = Field(..., gt=0)


class BillResponse(BaseModel):
    bill_id: int
    service_id: int
    customer_id: int
    vehicle_id: int
    labour_charge: Decimal
    spare_parts_charge: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    final_amount: Decimal
    paid_amount: Decimal
    payment_status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)