from rest_framework.routers import DefaultRouter

from .views import (
    ServiceViewSet,
    DoctorServiceViewSet,
)


router = DefaultRouter()

router.register(
    "services",
    ServiceViewSet,
    basename="services",
)

router.register(
    "doctor-services",
    DoctorServiceViewSet,
    basename="doctor-services",
)

urlpatterns = router.urls
