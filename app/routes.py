from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DoctorViewSet, AppointmentViewSet, TreatmentViewSet, ReviewViewSet ,  MedicationViewSet, HealthReportViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'treatments', TreatmentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'medications', MedicationViewSet, basename='medication')
router.register(r'health-reports', HealthReportViewSet, basename='healthreport')
urlpatterns = router.urls