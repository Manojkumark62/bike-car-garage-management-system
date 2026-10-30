from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.mechanic_management.models import Mechanic
from src.mechanic_management.schemas import MechanicCreate, MechanicUpdate


def create_mechanic(db: Session, mechanic: MechanicCreate):

    existing_mechanic = db.query(Mechanic).filter(Mechanic.contact_number == mechanic.contact_number).first()
    if existing_mechanic:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contact number already exists")
    
    db_mechanic = Mechanic(
        mechanic_name=mechanic.mechanic_name,
        contact_number=mechanic.contact_number,
        specialization=mechanic.specialization,
        experience=mechanic.experience
    )

    db.add(db_mechanic)
    db.commit()
    db.refresh(db_mechanic)

    return db_mechanic


def get_mechanics(db: Session):
    return db.query(Mechanic).all()


def get_mechanic_by_id(db: Session, mechanic_id: int):
    mechanic = db.query(Mechanic).filter(Mechanic.mechanic_id == mechanic_id).first()

    if not mechanic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mechanic not found")

    return mechanic


def update_mechanic(db: Session, mechanic_id: int, mechanic: MechanicUpdate):
    db_mechanic = db.query(Mechanic).filter(Mechanic.mechanic_id == mechanic_id).first()

    if not db_mechanic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mechanic not found")

    update_data = mechanic.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_mechanic, field, value)

    db.commit()
    db.refresh(db_mechanic)

    return db_mechanic


def delete_mechanic(db: Session, mechanic_id: int):
    db_mechanic = db.query(Mechanic).filter(Mechanic.mechanic_id == mechanic_id).first()

    if not db_mechanic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mechanic not found")

    db.delete(db_mechanic)
    db.commit()

    return {"message": "Mechanic deleted successfully"}