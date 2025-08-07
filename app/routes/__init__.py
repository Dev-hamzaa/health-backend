from fastapi import APIRouter
from app.routes.patient_route import router as patient_router
from app.routes.doctor_route import router as doctor_router
# You can also import others like doctor_router, appointment_router here

router = APIRouter()

router.include_router(patient_router)
router.include_router(doctor_router)

