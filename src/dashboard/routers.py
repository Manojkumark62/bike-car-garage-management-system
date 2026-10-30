from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.dashboard.schemas import DashboardResponse
from src.dashboard.services import get_dashboard_data


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    return get_dashboard_data(db)