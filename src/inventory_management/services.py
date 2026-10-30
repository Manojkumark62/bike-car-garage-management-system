from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.inventory_management.models import SparePart
from src.service_management.models import Service
from src.inventory_management.schemas import SparePartCreate, SparePartUpdate


def create_spare_part(db: Session, spare_part_data: SparePartCreate):
    existing_spare_part = db.query(SparePart).filter(SparePart.part_number == spare_part_data.part_number).first()

    if existing_spare_part:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Part number already exists")

    if spare_part_data.minimum_stock_level < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Minimum stock level cannot be negative")

    if spare_part_data.available_quantity < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Available quantity cannot be negative")

    if spare_part_data.price < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price cannot be negative")

    spare_part = SparePart(part_name=spare_part_data.part_name, part_number=spare_part_data.part_number, category=spare_part_data.category, available_quantity=spare_part_data.available_quantity, price=spare_part_data.price, minimum_stock_level=spare_part_data.minimum_stock_level)

    db.add(spare_part)
    db.commit()
    db.refresh(spare_part)

    return spare_part


def get_all_spare_parts(db: Session):
    return db.query(SparePart).all()


def get_spare_part_by_id(db: Session, part_id: int):
    spare_part = db.query(SparePart).filter(SparePart.part_id == part_id).first()

    if not spare_part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spare part not found")

    return spare_part


def search_spare_part_by_number(db: Session, part_number: str):
    part_number = part_number.strip()

    spare_part = db.query(SparePart).filter(SparePart.part_number.ilike(part_number)).first()

    if not spare_part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spare part not found")

    return spare_part


def update_spare_part(db: Session, part_id: int, spare_part_data: SparePartUpdate):
    spare_part = db.query(SparePart).filter(SparePart.part_id == part_id).first()

    if not spare_part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spare part not found")

    update_data = spare_part_data.model_dump(exclude_unset=True)

    if "part_number" in update_data:
        existing_part = db.query(SparePart).filter(SparePart.part_number == update_data["part_number"], SparePart.part_id != part_id).first()

        if existing_part:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Part number already exists")

    if "available_quantity" in update_data and update_data["available_quantity"] < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Available quantity cannot be negative")

    if "minimum_stock_level" in update_data and update_data["minimum_stock_level"] < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Minimum stock level cannot be negative")

    if "price" in update_data and update_data["price"] < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price cannot be negative")

    for field, value in update_data.items():
        setattr(spare_part, field, value)

    db.commit()
    db.refresh(spare_part)

    return spare_part


def delete_spare_part(db: Session, part_id: int):
    spare_part = db.query(SparePart).filter(SparePart.part_id == part_id).first()

    if not spare_part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spare part not found")

    existing_service_part = db.query(ServicePart).filter(ServicePart.part_id == part_id).first()

    if existing_service_part:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spare part cannot be deleted because it is used in a service")

    db.delete(spare_part)
    db.commit()

    return {"message": "Spare part deleted successfully"}


def get_low_stock_parts(db: Session):
    return db.query(SparePart).filter(SparePart.available_quantity <= SparePart.minimum_stock_level).all()