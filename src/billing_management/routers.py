from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.billing_management.schemas import BillCreate, BillResponse, PaymentUpdate
from src.billing_management.services import generate_bill, get_bill_by_id, get_bill_by_service, get_all_bills, update_payment


router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
def generate_bill_api(bill_data: BillCreate, db: Session = Depends(get_db)):
    return generate_bill(db, bill_data)


@router.get("/", response_model=list[BillResponse])
def get_all_bills_api(db: Session = Depends(get_db)):
    return get_all_bills(db)


@router.get("/{bill_id}", response_model=BillResponse)
def get_bill_api(bill_id: int, db: Session = Depends(get_db)):
    return get_bill_by_id(db, bill_id)


@router.get("/service/{service_id}", response_model=BillResponse)
def get_bill_by_service_api(service_id: int, db: Session = Depends(get_db)):
    return get_bill_by_service(db, service_id)


@router.put("/{bill_id}/payment", response_model=BillResponse)
def update_payment_api(bill_id: int, payment_data: PaymentUpdate, db: Session = Depends(get_db)):
    return update_payment(db, bill_id, payment_data)