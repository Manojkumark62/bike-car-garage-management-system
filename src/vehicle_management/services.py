from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.vehicle_management.models import Vehicle
from src.customer_management.models import Customer
from src.vehicle_management.schemas import CreateVehicleRequest, UpdateVehicleRequest


def create_vehicle(db: Session, vehicle_data: CreateVehicleRequest):
    customer = db.query(Customer).filter(Customer.cust_id == vehicle_data.customer_id).first()

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    existing_vehicle = db.query(Vehicle).filter(Vehicle.registration_number == vehicle_data.registration_number).first()

    if existing_vehicle:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration number already exists")

    vehicle = Vehicle(customer_id=vehicle_data.customer_id, registration_number=vehicle_data.registration_number, vehicle_type=vehicle_data.vehicle_type, brand=vehicle_data.brand, model=vehicle_data.model, fuel_type=vehicle_data.fuel_type)

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle


def get_all_vehicles(db: Session):
    return db.query(Vehicle).all()


def get_vehicle_by_id(db: Session, vehicle_id: int):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    return vehicle


def search_vehicle_by_registration_number(db: Session, registration_number: str):
    vehicle = db.query(Vehicle).filter(Vehicle.registration_number == registration_number).first()

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    return vehicle


def update_vehicle(db: Session, vehicle_id: int, vehicle_data: UpdateVehicleRequest):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    update_data = vehicle_data.model_dump(exclude_unset=True)

    if "customer_id" in update_data:
        customer = db.query(Customer).filter(Customer.cust_id == update_data["customer_id"]).first()

        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    if "registration_number" in update_data:
        existing_vehicle = db.query(Vehicle).filter(Vehicle.registration_number == update_data["registration_number"], Vehicle.vehicle_id != vehicle_id).first()

        if existing_vehicle:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration number already exists")

    for field, value in update_data.items():
        setattr(vehicle, field, value)

    db.commit()
    db.refresh(vehicle)

    return vehicle


def delete_vehicle(db: Session, vehicle_id: int):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    db.delete(vehicle)
    db.commit()

    return {"message": "Vehicle deleted successfully"}