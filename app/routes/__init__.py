from .doctor_route import router as doctor_router
from .patient_route import router as patient_router
from .appointment_route import router as appointment_router
from .reviews_route import router as review_router

__all__ = ["doctor_router", "patient_router", "appointment_router", "review_router"]
