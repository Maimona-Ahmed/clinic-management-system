from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny

from .models import Service, DoctorService

from .serializers import (
    ServiceSerializer,
    ServiceDetailSerializer,
    DoctorServiceSerializer,
)

from .permissions import (
    IsAdminUser,
    IsAdminOrDoctorOwner,
)


class ServiceViewSet(viewsets.ModelViewSet):

    queryset = Service.objects.all()

    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get(
            "is_active"
        )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active
            )

        return queryset

    def get_permissions(self):

        if self.action in [
            "list",
            "retrieve",
        ]:
            permission_classes = [
                AllowAny
            ]

        else:
            permission_classes = [
                IsAdminUser
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def get_serializer_class(self):

        if self.action == "retrieve":
            return ServiceDetailSerializer

        return ServiceSerializer


class DoctorServiceViewSet(viewsets.ModelViewSet):

    queryset = (
        DoctorService.objects
        .select_related(
            "doctor__user",
            "service",
        )
    )

    serializer_class = (
        DoctorServiceSerializer
    )

    def get_queryset(self):

        queryset = super().get_queryset()

        service_id = (
            self.request.query_params.get(
                "service"
            )
        )

        doctor_id = (
            self.request.query_params.get(
                "doctor"
            )
        )

        if service_id:
            queryset = queryset.filter(
                service_id=service_id
            )

        if doctor_id:
            queryset = queryset.filter(
                doctor_id=doctor_id
            )

        return queryset

    def get_permissions(self):

        if self.action in [
            "list",
            "retrieve",
        ]:
            permission_classes = [
                AllowAny
            ]

        else:
            permission_classes = [
                IsAdminOrDoctorOwner
            ]

        return [
            permission()
            for permission
            in permission_classes
        ]

    def perform_create(
        self,
        serializer,
    ):

        doctor = (
            serializer.validated_data["doctor"]
        )

        if self.request.user.is_superuser:
            serializer.save()
            return
        if doctor.user != self.request.user:
            raise PermissionDenied(
                "You can only create "
                "services for yourself."
            )

        serializer.save()
