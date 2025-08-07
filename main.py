from fastapi import FastAPI
from config.database import Base, engine
from app.routes import  patient_router, appointment_router, review_router

app = FastAPI(
    title="Hospital Management API",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)


app.include_router(patient_router)
app.include_router(appointment_router)
app.include_router(review_router)
