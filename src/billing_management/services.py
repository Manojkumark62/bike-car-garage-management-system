from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.service_management.models import Service, ServicePart
from src.customer_management.models import Customer
from src.vehicle_management.models import Vehicle
from src.billing_management.models import Bill
from src.billing_management.schemas import BillCreate, PaymentUpdate


def generate_bill(db: Session, bill_data: BillCreate):
    service = db.query(Service).filter(Service.service_id == bill_data.service_id).first()

    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    existing_bill = db.query(Bill).filter(Bill.service_id == bill_data.service_id).first()

    if existing_bill:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bill already exists for this service")

    customer = db.query(Customer).filter(Customer.cust_id == service.customer_id).first()

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == service.vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    service_parts = db.query(ServicePart).filter(ServicePart.service_id == service.service_id).all()

    spare_parts_charge = sum((part.unit_price * part.quantity for part in service_parts), Decimal("0.00"))

    labour_charge = Decimal(str(service.labour_charge or 0))
    tax_amount = Decimal(str(bill_data.tax_amount or 0))
    discount_amount = Decimal(str(bill_data.discount_amount or 0))

    final_amount = labour_charge + spare_parts_charge + tax_amount - discount_amount

    if final_amount < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Discount cannot be greater than total charges")

    bill = Bill(
        service_id=service.service_id,
        customer_id=service.customer_id,
        vehicle_id=service.vehicle_id,
        labour_charge=labour_charge,
        spare_parts_charge=spare_parts_charge,
        tax_amount=tax_amount,
        discount_amount=discount_amount,
        final_amount=final_amount,
        paid_amount=Decimal("0.00"),
        payment_status="Pending"
    )

    db.add(bill)
    db.commit()
    db.refresh(bill)

    return bill


def get_bill_by_id(db: Session, bill_id: int):
    bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()

    if not bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")

    return bill


def get_bill_by_service(db: Session, service_id: int):
    bill = db.query(Bill).filter(Bill.service_id == service_id).first()

    if not bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")

    return bill


def get_all_bills(db: Session):
    return db.query(Bill).order_by(Bill.created_at.desc()).all()


def update_payment(db: Session, bill_id: int, payment_data: PaymentUpdate):
    bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()

    if not bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")

    new_paid_amount = Decimal(str(bill.paid_amount or 0)) + Decimal(str(payment_data.paid_amount))

    if new_paid_amount > bill.final_amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment cannot be greater than final bill amount")

    bill.paid_amount = new_paid_amount

    if new_paid_amount == 0:
        bill.payment_status = "Pending"
    elif new_paid_amount < bill.final_amount:
        bill.payment_status = "Partially Paid"
    else:
        bill.payment_status = "Paid"

    db.commit()
    db.refresh(bill)

    return bill