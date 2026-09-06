from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentViewSet,
    DoctorSlotView,
)


router = DefaultRouter()

router.register(
    "appointments",
    AppointmentViewSet,
    basename="appointment",
)


urlpatterns = router.urls


urlpatterns += [
    path(
        "doctor-slots/",
        DoctorSlotView.as_view(),
        name="doctor-slots",
    ),
]
