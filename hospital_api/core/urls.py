from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import UserViewSet, DoctorViewSet, PatientViewSet, AssistantViewSet, TreatmentViewSet, patient_treatments_report, doctors_report
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'assistants', AssistantViewSet, basename='assistant')
router.register(r'treatments', TreatmentViewSet, basename='treatment')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("reports/patient/<int:patient_id>/treatments/", patient_treatments_report, name="patient-treatments-report"),
    path("reports/doctors/", doctors_report, name="doctors-report"),
]