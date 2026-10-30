from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.mechanic_management.schemas import MechanicCreate, MechanicResponse, MechanicUpdate
from src.mechanic_management.services import create_mechanic, get_mechanics, get_mechanic_by_id, update_mechanic, delete_mechanic

router = APIRouter(prefix="/mechanics", tags=["Mechanics"])


@router.post("/", response_model=MechanicResponse, status_code=status.HTTP_201_CREATED)
def create(mechanic: MechanicCreate, db: Session = Depends(get_db)):
    return create_mechanic(db, mechanic)


@router.get("/", response_model=list[MechanicResponse])
def get_all(db: Session = Depends(get_db)):
    return get_mechanics(db)


@router.get("/{mechanic_id}", response_model=MechanicResponse)
def get_by_id(mechanic_id: int, db: Session = Depends(get_db)):
    return get_mechanic_by_id(db, mechanic_id)


@router.put("/{mechanic_id}", response_model=MechanicResponse)
def update(mechanic_id: int, mechanic: MechanicUpdate, db: Session = Depends(get_db)):
    return update_mechanic(db, mechanic_id, mechanic)


@router.delete("/{mechanic_id}", status_code=status.HTTP_200_OK)
def delete(mechanic_id: int, db: Session = Depends(get_db)):
    return delete_mechanic(db, mechanic_id)