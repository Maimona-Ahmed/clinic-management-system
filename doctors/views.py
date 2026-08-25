from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import DoctorProfile,DoctorSchedule,DoctorTimeOff
from .permissions import IsAdminUser,DoctorSchedulePermission
from .serializers import (
    DoctorSerializer,
    DoctorCreateSerializer,
    DoctorScheduleSerializer,
    DoctorTimeOffSerializer
    
)


class DoctorViewSet(viewsets.ModelViewSet):

    queryset = DoctorProfile.objects.select_related("user")

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]

        return [
            permission()
            for permission in permission_classes
        ]

    def get_serializer_class(self):
        if self.action == "create":
            return DoctorCreateSerializer

        return DoctorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        doctor = serializer.save()

        response_serializer = DoctorSerializer(
            doctor,
            context=self.get_serializer_context()
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def perform_destroy(self, instance):
        user = instance.user

        instance.delete()
        user.delete()




class DoctorScheduleViewSet(
    viewsets.ModelViewSet
):

    serializer_class = (
        DoctorScheduleSerializer
    )

    permission_classes = [
        DoctorSchedulePermission
    ]

    def get_queryset(self):

        user = self.request.user

        if user.is_superuser:
            return (
                DoctorSchedule.objects
                .select_related("doctor")
                .all()
            )

        if hasattr(
            user,
            "doctor_profile",
        ):
            return (
                DoctorSchedule.objects
                .select_related("doctor")
                .filter(
                    doctor=user.doctor_profile
                )
            )

        return DoctorSchedule.objects.none()

    def perform_create(
        self,
        serializer,
    ):

        serializer.save(
            doctor=(
                self.request
                .user
                .doctor_profile
            )
        )



class DoctorTimeOffViewSet(viewsets.ModelViewSet):

    serializer_class = DoctorTimeOffSerializer

    permission_classes = [
        DoctorSchedulePermission
    ]

    def get_queryset(self):

        user = self.request.user

        if user.is_superuser:
            return (
                DoctorTimeOff.objects
                .select_related("doctor")
                .all()
            )

        if hasattr(user, "doctor_profile"):
            return (
                DoctorTimeOff.objects
                .select_related("doctor")
                .filter(
                    doctor=user.doctor_profile
                )
            )

        return DoctorTimeOff.objects.none()

    def perform_create(self, serializer):

        serializer.save(
            doctor=self.request.user.doctor_profile
        )
