from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db

from src.customer_management.schemas import CreateCustomerRequest, UpdateCustomerRequest, CustomerResponse, CustomerListResponse
from src.customer_management.services import create_customer, get_customer, get_all_customers, update_customer, delete_customer

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer_route(request: CreateCustomerRequest, db: Session = Depends(get_db)):
    return create_customer(db, request)


@router.get("/", response_model=CustomerListResponse)
def get_all_customers_route(db: Session = Depends(get_db)):
    return get_all_customers(db)


@router.get("/{cust_id}", response_model=CustomerResponse)
def get_customer_route(cust_id: int, db: Session = Depends(get_db)):
    return get_customer(db, cust_id)


@router.put("/{cust_id}", response_model=CustomerResponse)
def update_customer_route(
    cust_id: int,
    request: UpdateCustomerRequest,
    db: Session = Depends(get_db)
):
    return update_customer(db, cust_id, request)


@router.delete("/{cust_id}")
def delete_customer_route(cust_id: int, db: Session = Depends(get_db)):
    return delete_customer(db, cust_id)
