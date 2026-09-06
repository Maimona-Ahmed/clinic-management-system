from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    DoctorViewSet,
    DoctorScheduleViewSet,
    DoctorTimeOffViewSet,
    DoctorDashboardView,
)


router = DefaultRouter()

router.register(
    "doctors",
    DoctorViewSet,
    basename="doctor",
)

router.register(
    "doctor-schedules",
    DoctorScheduleViewSet,
    basename="doctor-schedule",
)

router.register(
    "doctor-time-offs",
    DoctorTimeOffViewSet,
    basename="doctor-time-off",
)


urlpatterns = [
    path(
        "doctors/dashboard/",
        DoctorDashboardView.as_view(),
        name="doctor-dashboard",
    ),
]

urlpatterns += router.urls