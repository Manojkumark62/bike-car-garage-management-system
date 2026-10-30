from fastapi import FastAPI
from src.database import Base, engine

from src.customer_management.routers import router as customer_router
from src.vehicle_management.routers import router as vehicle_router
from src.service_management.routers import router as service_router
from src.mechanic_management.routers import router as mechanic_router
from src.inventory_management.routers import router as inventory_router
from src.billing_management.routers import router as billing_router
from src.dashboard.routers import router as dashboard_router

app = FastAPI(title="Bike & Car Garage Customer Management API", swagger_ui_parameters={"operationsSorter": "alpha"})
Base.metadata.create_all(bind=engine)

app.include_router(customer_router)
app.include_router(vehicle_router)
app.include_router(mechanic_router)
app.include_router(service_router)
app.include_router(inventory_router)
app.include_router(billing_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"message": "Bike & Car Garage Customer API is running"}