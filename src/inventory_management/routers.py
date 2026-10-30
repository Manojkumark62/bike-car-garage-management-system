from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.inventory_management.schemas import SparePartCreate, SparePartUpdate, SparePartResponse, SparePartListResponse
from src.inventory_management.services import create_spare_part, get_all_spare_parts, get_spare_part_by_id, search_spare_part_by_number, update_spare_part, delete_spare_part, get_low_stock_parts

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("/", response_model=SparePartResponse, status_code=status.HTTP_201_CREATED)
def create_spare_part_api(spare_part_data: SparePartCreate, db: Session = Depends(get_db)):
    return create_spare_part(db, spare_part_data)


@router.get("/", response_model=SparePartListResponse)
def get_all_spare_parts_api(db: Session = Depends(get_db)):
    spare_parts = get_all_spare_parts(db)
    return {"spare_parts": spare_parts}


@router.get("/search/{part_number}", response_model=SparePartResponse)
def search_spare_part_api(part_number: str, db: Session = Depends(get_db)):
    return search_spare_part_by_number(db, part_number)


@router.get("/low-stock", response_model=SparePartListResponse)
def get_low_stock_parts_api(db: Session = Depends(get_db)):
    spare_parts = get_low_stock_parts(db)
    return {"spare_parts": spare_parts}


@router.get("/{part_id}", response_model=SparePartResponse)
def get_spare_part_api(part_id: int, db: Session = Depends(get_db)):
    return get_spare_part_by_id(db, part_id)


@router.put("/{part_id}", response_model=SparePartResponse)
def update_spare_part_api(part_id: int, spare_part_data: SparePartUpdate, db: Session = Depends(get_db)):
    return update_spare_part(db, part_id, spare_part_data)


@router.delete("/{part_id}")
def delete_spare_part_api(part_id: int, db: Session = Depends(get_db)):
    return delete_spare_part(db, part_id)