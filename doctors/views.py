from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from datetime import date

from django.db.models import Count, Q

from rest_framework import status
from rest_framework.views import APIView

from appointments.models import Appointment


from .models import DoctorProfile,DoctorSchedule,DoctorTimeOff
from .permissions import IsAdminUser,DoctorSchedulePermission
from .serializers import (
    DoctorSerializer,
    DoctorCreateSerializer,
    DoctorScheduleSerializer,
    DoctorTimeOffSerializer,
    DashboardStatisticsSerializer,
    DashboardAppointmentSerializer,
    
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



class DoctorDashboardView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        return Response({
            "message": "Doctor Dashboard works!"
        })

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        # ==========================================
        # 1. Current Doctor
        # ==========================================

        if not hasattr(
            request.user,
            "doctor_profile",
        ):

            return Response(
                {
                    "detail": (
                        "Only doctors can access "
                        "the doctor dashboard."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        doctor = request.user.doctor_profile

        # ==========================================
        # 2. Doctor Appointments
        # ==========================================

        appointments = (
            Appointment.objects
            .select_related(
                "patient",
                "patient__user",
                "doctor",
                "doctor_service",
                "doctor_service__service",
            )
            .filter(
                doctor=doctor
            )
        )

        # ==========================================
        # 3. Today
        # ==========================================

        today = date.today()

        # ==========================================
        # 4. Statistics
        # ==========================================

        statistics = appointments.aggregate(

            total_appointments=Count(
                "id"
            ),

            today_appointments=Count(
                "id",
                filter=Q(
                    appointment_date=today
                ),
            ),

            pending_appointments=Count(
                "id",
                filter=Q(
                    status=Appointment.Status.PENDING
                ),
            ),

            confirmed_appointments=Count(
                "id",
                filter=Q(
                    status=Appointment.Status.CONFIRMED
                ),
            ),

            completed_appointments=Count(
                "id",
                filter=Q(
                    status=Appointment.Status.COMPLETED
                ),
            ),

            cancelled_appointments=Count(
                "id",
                filter=Q(
                    status=Appointment.Status.CANCELLED
                ),
            ),
        )

        # ==========================================
        # 5. Statistics Serializer
        # ==========================================

        statistics_serializer = (
            DashboardStatisticsSerializer(
                statistics
            )
        )

        # ==========================================
        # 6. Today's Appointments
        # ==========================================

        today_appointments = (
            appointments
            .filter(
                appointment_date=today
            )
            .order_by(
                "appointment_time"
            )
        )

        # ==========================================
        # 7. Today's Appointments Serializer
        # ==========================================

        today_serializer = (
            DashboardAppointmentSerializer(
                today_appointments,
                many=True,
            )
        )

        # ==========================================
        # 8. Response
        # ==========================================

        return Response(
            {
                "statistics":
                    statistics_serializer.data,

                "today_appointments":
                    today_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

