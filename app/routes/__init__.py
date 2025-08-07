from fastapi import APIRouter
from app.routes.patient_route import router as patient_router
from app.routes.doctor_route import router as doctor_router
from app.routes.appointment_route import router as appointment_router
from app.routes.reviews_route import router as reviews_router
# You can also import others like doctor_router, appointment_router here

router = APIRouter()

router.include_router(patient_router)
router.include_router(doctor_router)
router.include_router(appointment_router)
router.include_router(reviews_router)

