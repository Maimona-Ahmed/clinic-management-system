from django.urls import (
    include,
    path,
)

from rest_framework.routers import (
    DefaultRouter,
)

from .views import (
    ConsultationViewSet,
    PrescriptionItemViewSet,
)


router = DefaultRouter()

router.register(
    "consultations",
    ConsultationViewSet,
    basename="consultation",
)

router.register(
    "prescription-items",
    PrescriptionItemViewSet,
    basename="prescription-item",
)


urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
]
