from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.customer_management.models import Customer
from src.vehicle_management.models import Vehicle
from src.mechanic_management.models import Mechanic
from src.inventory_management.models import SparePart
from src.service_management.models import Service, ServiceHistory, ServicePart
from src.service_management.schemas import ServiceCreate, ServiceUpdate, ServicePartCreate


def create_service(db: Session, service: ServiceCreate):
    
    customer = db.query(Customer).filter(Customer.cust_id == service.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == service.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    if vehicle.customer_id != customer.cust_id:
        raise HTTPException(status_code=400, detail="Vehicle does not belong to this customer")

    mechanic = db.query(Mechanic).filter(Mechanic.mechanic_id == service.mechanic_id).first()
    if not mechanic:
        raise HTTPException(status_code = 404, detail = 'Mechanicnot found')

    db_service = Service(
        customer_id=service.customer_id,
        vehicle_id=service.vehicle_id,
        mechanic_id=service.mechanic_id,
        service_type=service.service_type,
        complaint=service.complaint,
        arrival_date=service.arrival_date,
        expected_delivery_date=service.expected_delivery_date,
        labour_charge=service.labour_charge,
        total_service_cost=service.total_service_cost,
        additional_notes=service.additional_notes
    )

    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    return db_service


def get_service_by_id(db: Session, service_id: int):
    service = db.query(Service).filter(Service.service_id == service_id).first()

    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    return service


def get_all_services(db: Session):
    return db.query(Service).all()


def update_service(db: Session, service_id: int, service_data: ServiceUpdate):
    service = db.query(Service).filter(Service.service_id == service_id).first()

    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    update_data = service_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(service, key, value)

    db.commit()
    db.refresh(service)

    return service


def assign_mechanic_to_service(db: Session, mechanic_id: int, service_id: int):
    service = db.query(Service).filter(Service.service_id == service_id).first()

    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    mechanic = db.query(Mechanic).filter(Mechanic.mechanic_id == mechanic_id).first()

    if not mechanic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mechanic not found")

    service.mechanic_id = mechanic_id

    history = ServiceHistory(service_id=service_id, mechanic_id=mechanic_id)

    db.add(history)
    db.commit()
    db.refresh(service)

    return service


def get_all_service_history(db: Session):
    return db.query(ServiceHistory).order_by(ServiceHistory.assigned_at.desc()).all()


def delete_service(db: Session, service_id: int):
    service = db.query(Service).filter(Service.service_id == service_id).first()

    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    db.query(ServiceHistory).filter(ServiceHistory.service_id == service_id).delete(synchronize_session=False)

    db.delete(service)
    db.commit()

    return {"message": "Service deleted successfully"}



def add_part_to_service(db: Session, service_id: int, part_data: ServicePartCreate):
    service = db.query(Service).filter(Service.service_id == service_id).first()

    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    spare_part = db.query(SparePart).filter(SparePart.part_id == part_data.part_id).first()

    if not spare_part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spare part not found")

    if spare_part.available_quantity < part_data.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient spare part stock")

    service_part = ServicePart(
        service_id=service_id, 
        part_id=part_data.part_id, 
        quantity=part_data.quantity, 
        unit_price=spare_part.price
        )

    spare_part.available_quantity -= part_data.quantity
    service.total_service_cost += spare_part.price * part_data.quantity

    db.add(service_part)
    db.commit()
    db.refresh(service_part)

    return service_part


def get_service_parts(db: Session, service_id: int):
    service = db.query(Service).filter(Service.service_id == service_id).first()

    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    service_parts = db.query(ServicePart).filter(ServicePart.service_id == service_id).all()

    if not service_parts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No spare parts have been added to this service")

    return service_parts


def delete_service_part(db: Session, service_part_id: int):
    service_part = db.query(ServicePart).filter(ServicePart.service_part_id == service_part_id).first()

    if not service_part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service part not found")

    spare_part = db.query(SparePart).filter(SparePart.part_id == service_part.part_id).first()

    service = db.query(Service).filter(Service.service_id == service_part.service_id).first()

    if spare_part:
        spare_part.available_quantity += service_part.quantity

    if service:
        service.total_service_cost -= service_part.unit_price * service_part.quantity

    db.delete(service_part)
    db.commit()

    return {"message": "Service part removed and stock restored successfully"}