from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.customer_management.models import Customer
from src.customer_management.schemas import CreateCustomerRequest, UpdateCustomerRequest, CustomerResponse, CustomerListResponse

def create_customer(db: Session, request: CreateCustomerRequest) -> CustomerResponse:
    existing_email = db.query(Customer).filter(Customer.email == request.email).first()
    if existing_email: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    existing_phone = db.query(Customer).filter(Customer.phone_number == request.phone_number).first()
    if existing_phone: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already exists")
    
    customer = Customer(name=request.name, email=request.email, phone_number=request.phone_number, address=request.address)
    
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return CustomerResponse.model_validate(customer)


def get_customer(db: Session, cust_id: int) -> CustomerResponse:
    customer = db.query(Customer).filter(Customer.cust_id == cust_id).first()
    if customer is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return CustomerResponse.model_validate(customer)


def get_all_customers(db: Session) -> CustomerListResponse:
    customers = db.query(Customer).all()
    return CustomerListResponse(customers=[CustomerResponse.model_validate(customer) for customer in customers])


def update_customer(db: Session, cust_id: int, request: UpdateCustomerRequest) -> CustomerResponse:
    customer = db.query(Customer).filter(Customer.cust_id == cust_id).first()

    if customer is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    update_data = request.model_dump(exclude_unset=True)
    
    if "email" in update_data:
        existing_email = db.query(Customer).filter(Customer.email == update_data["email"], Customer.cust_id != cust_id).first()
        if existing_email: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    if "phone_number" in update_data:
        existing_phone = db.query(Customer).filter(Customer.phone_number == update_data["phone_number"], Customer.cust_id != cust_id).first()
        if existing_phone: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already exists")
    
    for field, value in update_data.items(): 
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return CustomerResponse.model_validate(customer)


def delete_customer(db: Session, cust_id: int):
    customer = db.query(Customer).filter(Customer.cust_id == cust_id).first()
    if customer is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}