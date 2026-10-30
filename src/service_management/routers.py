from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.service_management.schemas import ServiceCreate, ServiceUpdate, ServiceResponse, ServiceHistoryResponse, ServicePartCreate, ServicePartResponse, ServicePartListResponse
from src.service_management.services import create_service, get_service_by_id, get_all_services, update_service, get_all_service_history, assign_mechanic_to_service, delete_service, add_part_to_service, get_service_parts, delete_service_part


router = APIRouter(prefix="/services", tags=["Services"])


@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service_api(service_data: ServiceCreate, db: Session = Depends(get_db)):
    return create_service(db, service_data)


@router.get("/", response_model=list[ServiceResponse])
def get_all_services_api(db: Session = Depends(get_db)):
    return get_all_services(db)


@router.get("/history", response_model=list[ServiceHistoryResponse])
def get_all_history(db: Session = Depends(get_db)):
    return get_all_service_history(db)


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service_api(service_id: int, db: Session = Depends(get_db)):
    return get_service_by_id(db, service_id)


@router.put("/{service_id}", response_model=ServiceResponse)
def update_service_api(service_id: int, service_data: ServiceUpdate, db: Session = Depends(get_db)):
    return update_service(db, service_id, service_data)


@router.put("/{service_id}/mechanic/{mechanic_id}", response_model=ServiceResponse)
def assign_mechanic(service_id: int, mechanic_id: int, db: Session = Depends(get_db)):
    return assign_mechanic_to_service(db, mechanic_id, service_id)


@router.delete("/{service_id}")
def delete_service_api(service_id: int, db: Session = Depends(get_db)):
    return delete_service(db, service_id)


@router.post("/{service_id}/parts", response_model=ServicePartResponse, status_code=status.HTTP_201_CREATED)
def add_part_to_service_api(service_id: int, part_data: ServicePartCreate, db: Session = Depends(get_db)):
    return add_part_to_service(db, service_id, part_data)


@router.get("/{service_id}/parts", response_model=ServicePartListResponse)
def get_service_parts_api(service_id: int, db: Session = Depends(get_db)):
    service_parts = get_service_parts(db, service_id)
    return {"service_parts": service_parts}


@router.delete("/{service_id}/parts/{service_part_id}")
def delete_service_part_api(service_id: int, service_part_id: int, db: Session = Depends(get_db)):
    return delete_service_part(db, service_part_id)