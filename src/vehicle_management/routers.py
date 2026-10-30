from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.vehicle_management.schemas import CreateVehicleRequest, UpdateVehicleRequest, VehicleResponse, VehicleListResponse
from src.vehicle_management.services import create_vehicle, get_all_vehicles, get_vehicle_by_id, update_vehicle, delete_vehicle, search_vehicle_by_registration_number

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle_api(vehicle_data: CreateVehicleRequest, db: Session = Depends(get_db)):
    return create_vehicle(db, vehicle_data)


@router.get("/", response_model=VehicleListResponse)
def get_all_vehicles_api(db: Session = Depends(get_db)):
    vehicles = get_all_vehicles(db)
    return {"vehicles": vehicles}


@router.get("/search/{registration_number}", response_model=VehicleResponse)
def search_vehicle_api(registration_number: str, db: Session = Depends(get_db)):
    return search_vehicle_by_registration_number(db, registration_number)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle_api(vehicle_id: int, db: Session = Depends(get_db)):
    return get_vehicle_by_id(db, vehicle_id)


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle_api(vehicle_id: int, vehicle_data: UpdateVehicleRequest, db: Session = Depends(get_db)):
    return update_vehicle(db, vehicle_id, vehicle_data)


@router.delete("/{vehicle_id}")
def delete_vehicle_api(vehicle_id: int, db: Session = Depends(get_db)):
    return delete_vehicle(db, vehicle_id)