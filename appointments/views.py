from rest_framework import (
    status,
    viewsets,
)

from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from .models import Appointment

from .permissions import AppointmentPermission

from .serializers import AppointmentSerializer

from .services import AppointmentService


class AppointmentViewSet(
    viewsets.ModelViewSet
):

    serializer_class = AppointmentSerializer

    permission_classes = [
        IsAuthenticated,
        AppointmentPermission,
    ]

    # ==================================================
    # QUERYSET
    # ==================================================

    def get_queryset(self):

        user = self.request.user

        # ----------------------------------------------
        # Patient
        # ----------------------------------------------

        if hasattr(
            user,
            "patient_profile",
        ):

            return (
                Appointment.objects
                .select_related(
                    "patient",
                    "doctor",
                    "doctor_service",
                    "doctor_service__service",
                )
                .filter(
                    patient=user.patient_profile
                )
                .order_by(
                    "-appointment_date",
                    "-appointment_time",
                )
            )

        # ----------------------------------------------
        # Doctor
        # ----------------------------------------------

        if hasattr(
            user,
            "doctor_profile",
        ):

            return (
                Appointment.objects
                .select_related(
                    "patient",
                    "doctor",
                    "doctor_service",
                    "doctor_service__service",
                )
                .filter(
                    doctor=user.doctor_profile
                )
                .order_by(
                    "-appointment_date",
                    "-appointment_time",
                )
            )

        return Appointment.objects.none()

    # ==================================================
    # CREATE
    # ==================================================

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

        # ----------------------------------------------
        # 1. Validate Input
        # ----------------------------------------------

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        # ----------------------------------------------
        # 2. Current Patient
        # ----------------------------------------------

        if not hasattr(
            request.user,
            "patient_profile",
        ):

            return Response(
                {
                    "detail":
                        "Only patients can create "
                        "appointments."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        patient = (
            request.user.patient_profile
        )

        # ----------------------------------------------
        # 3. Get Validated Data
        # ----------------------------------------------

        doctor_service = (
            serializer.validated_data[
                "doctor_service"
            ]
        )

        appointment_date = (
            serializer.validated_data[
                "appointment_date"
            ]
        )

        appointment_time = (
            serializer.validated_data[
                "appointment_time"
            ]
        )

        notes = (
            serializer.validated_data.get(
                "notes",
                "",
            )
        )

        # ----------------------------------------------
        # 4. Service
        # ----------------------------------------------

        appointment = (
            AppointmentService
            .create_appointment(
                patient=patient,
                doctor_service=doctor_service,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                notes=notes,
            )
        )

        # ----------------------------------------------
        # 5. Response
        # ----------------------------------------------

        output_serializer = (
            self.get_serializer(
                appointment
            )
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(
        self,
        request,
        *args,
        **kwargs,
    ):

        partial = kwargs.pop(
            "partial",
            False,
        )

        return self._update_appointment(
            request,
            partial=partial,
            *args,
            **kwargs,
        )

    # ==================================================
    # PARTIAL UPDATE
    # ==================================================

    def partial_update(
        self,
        request,
        *args,
        **kwargs,
    ):

        kwargs["partial"] = True

        return self.update(
            request,
            *args,
            **kwargs,
        )

    # ==================================================
    # UPDATE HELPER
    # ==================================================

    def _update_appointment(
        self,
        request,
        partial=False,
        *args,
        **kwargs,
    ):

        # ----------------------------------------------
        # 1. Get Appointment
        # ----------------------------------------------

        appointment = self.get_object()

        # ----------------------------------------------
        # 2. Validate Input
        # ----------------------------------------------

        serializer = self.get_serializer(
            appointment,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True
        )

        # ----------------------------------------------
        # 3. Get Values
        # ----------------------------------------------

        doctor_service = (
            serializer.validated_data.get(
                "doctor_service",
                appointment.doctor_service,
            )
        )

        appointment_date = (
            serializer.validated_data.get(
                "appointment_date",
                appointment.appointment_date,
            )
        )

        appointment_time = (
            serializer.validated_data.get(
                "appointment_time",
                appointment.appointment_time,
            )
        )

        notes = (
            serializer.validated_data.get(
                "notes",
                appointment.notes,
            )
        )

        # ----------------------------------------------
        # 4. Service
        # ----------------------------------------------

        appointment = (
            AppointmentService
            .update_appointment(
                appointment=appointment,
                doctor_service=doctor_service,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                notes=notes,
            )
        )

        # ----------------------------------------------
        # 5. Response
        # ----------------------------------------------

        output_serializer = (
            self.get_serializer(
                appointment
            )
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_200_OK,
        )

    # ==================================================
    # DELETE
    # ==================================================

    def destroy(
        self,
        request,
        *args,
        **kwargs,
    ):

        appointment = self.get_object()

        appointment.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    # ==================================================
    # CONFIRM
    # ==================================================

    @action(
        detail=True,
        methods=["post"],
    )
    def confirm(
        self,
        request,
        pk=None,
    ):

        # ----------------------------------------------
        # 1. Get Appointment
        # ----------------------------------------------

        appointment = self.get_object()

        # ----------------------------------------------
        # 2. Confirm + Create Invoice
        # ----------------------------------------------

        appointment, invoice = (
            AppointmentService
            .confirm_appointment(
                appointment=appointment,
            )
        )

        # ----------------------------------------------
        # 3. Serialize Appointment
        # ----------------------------------------------

        appointment_serializer = (
            self.get_serializer(
                appointment
            )
        )

        # ----------------------------------------------
        # 4. Response
        # ----------------------------------------------

        return Response(
            {
                "appointment":
                    appointment_serializer.data,

                "invoice": {
                    "id": invoice.id,
                    "amount": invoice.amount,
                    "status": invoice.status,
                },
            },
            status=status.HTTP_200_OK,
        )

    # ==================================================
    # CANCEL
    # ==================================================

    @action(
        detail=True,
        methods=["post"],
    )
    def cancel(
        self,
        request,
        pk=None,
    ):

        # ----------------------------------------------
        # 1. Get Appointment
        # ----------------------------------------------

        appointment = self.get_object()

        # ----------------------------------------------
        # 2. Cancel
        # ----------------------------------------------

        appointment = (
            AppointmentService
            .cancel_appointment(
                appointment=appointment,
            )
        )

        # ----------------------------------------------
        # 3. Serialize
        # ----------------------------------------------

        serializer = self.get_serializer(
            appointment
        )

        # ----------------------------------------------
        # 4. Response
        # ----------------------------------------------

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
            
