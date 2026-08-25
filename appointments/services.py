from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from doctors.models import (
    DoctorSchedule,
    DoctorTimeOff,
)
from services.models import DoctorService

from payments.services import create_invoice

from .models import Appointment


class AppointmentService:

    # ==================================================
    # CREATE APPOINTMENT
    # ==================================================

    @staticmethod
    @transaction.atomic
    def create_appointment(
        *,
        patient,
        doctor_service,
        appointment_date,
        appointment_time,
        notes="",
    ):

        # ----------------------------------------------
        # 1. Lock DoctorService
        # ----------------------------------------------

        doctor_service = (
            DoctorService.objects
            .select_for_update()
            .select_related(
                "doctor",
                "service",
            )
            .get(
                pk=doctor_service.pk
            )
        )

        # ----------------------------------------------
        # 2. Check DoctorService
        # ----------------------------------------------

        if not doctor_service.is_active:
            raise ValidationError({
                "doctor_service":
                    "This doctor service is not active."
            })

        # Doctor comes from DoctorService
        doctor = doctor_service.doctor

        # ----------------------------------------------
        # 3. Check Time Off
        # ----------------------------------------------

        has_time_off = (
            DoctorTimeOff.objects
            .filter(
                doctor=doctor,
                is_active=True,
                start_date__lte=appointment_date,
                end_date__gte=appointment_date,
            )
            .exists()
        )

        if has_time_off:
            raise ValidationError({
                "appointment_date":
                    "Doctor is not available on this date."
            })

        # ----------------------------------------------
        # 4. Check Schedule
        # ----------------------------------------------

        weekday = appointment_date.weekday()

        schedule = (
            DoctorSchedule.objects
            .filter(
                doctor=doctor,
                day_of_week=weekday,
                is_active=True,
            )
            .order_by(
                "start_time"
            )
            .first()
        )

        if not schedule:
            raise ValidationError({
                "appointment_date":
                    "Doctor does not work on this day."
            })

        # ----------------------------------------------
        # 5. Check Working Hours
        # ----------------------------------------------

        if not (
            schedule.start_time
            <= appointment_time
            < schedule.end_time
        ):
            raise ValidationError({
                "appointment_time":
                    "Appointment time is outside "
                    "doctor's working hours."
            })

        # ----------------------------------------------
        # 6. Check Doctor Slot
        # ----------------------------------------------

        doctor_conflict = (
            Appointment.objects
            .select_for_update()
            .filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=[
                    Appointment.Status.PENDING,
                    Appointment.Status.CONFIRMED,
                ],
            )
            .exists()
        )

        if doctor_conflict:
            raise ValidationError({
                "appointment_time":
                    "This time slot is already booked."
            })

        # ----------------------------------------------
        # 7. Check Patient Conflict
        # ----------------------------------------------

        patient_conflict = (
            Appointment.objects
            .filter(
                patient=patient,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=[
                    Appointment.Status.PENDING,
                    Appointment.Status.CONFIRMED,
                ],
            )
            .exists()
        )

        if patient_conflict:
            raise ValidationError({
                "appointment_time":
                    "Patient already has an appointment "
                    "at this time."
            })

        # ----------------------------------------------
        # 8. Create Appointment
        # ----------------------------------------------

        try:

            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                doctor_service=doctor_service,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status=Appointment.Status.PENDING,
                notes=notes,
            )

        except IntegrityError:

            raise ValidationError({
                "appointment_time":
                    "This time slot was just booked "
                    "by another request."
            })

        return appointment

    # ==================================================
    # CONFIRM APPOINTMENT
    # ==================================================

    @staticmethod
    @transaction.atomic
    def confirm_appointment(
        *,
        appointment,
    ):

        # ----------------------------------------------
        # 1. Lock Appointment
        # ----------------------------------------------

        appointment = (
            Appointment.objects
            .select_for_update()
            .select_related(
                "patient",
                "doctor",
                "doctor_service",
                "doctor_service__service",
            )
            .get(
                pk=appointment.pk
            )
        )

        # ----------------------------------------------
        # 2. Check Status
        # ----------------------------------------------

        if (
            appointment.status
            != Appointment.Status.PENDING
        ):
            raise ValidationError({
                "status":
                    "Only pending appointments "
                    "can be confirmed."
            })

        # ----------------------------------------------
        # 3. Confirm Appointment
        # ----------------------------------------------

        appointment.status = (
            Appointment.Status.CONFIRMED
        )

        appointment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        # ----------------------------------------------
        # 4. Create Invoice
        # ----------------------------------------------

        invoice = create_invoice(
            appointment=appointment
        )

        return appointment, invoice

    # ==================================================
    # UPDATE APPOINTMENT
    # ==================================================

    @staticmethod
    @transaction.atomic
    def update_appointment(
        *,
        appointment,
        doctor_service,
        appointment_date,
        appointment_time,
        notes,
    ):

        # ----------------------------------------------
        # 1. Lock Appointment
        # ----------------------------------------------

        appointment = (
            Appointment.objects
            .select_for_update()
            .select_related(
                "patient",
                "doctor",
                "doctor_service",
                "doctor_service__service",
            )
            .get(
                pk=appointment.pk
            )
        )

        # ----------------------------------------------
        # 2. Lock DoctorService
        # ----------------------------------------------

        doctor_service = (
            DoctorService.objects
            .select_for_update()
            .select_related(
                "doctor",
                "service",
            )
            .get(
                pk=doctor_service.pk
            )
        )

        # ----------------------------------------------
        # 3. Check DoctorService
        # ----------------------------------------------

        if not doctor_service.is_active:
            raise ValidationError({
                "doctor_service":
                    "This doctor service is not active."
            })

        # Doctor comes from DoctorService
        doctor = doctor_service.doctor

        # ----------------------------------------------
        # 4. Check Time Off
        # ----------------------------------------------

        has_time_off = (
            DoctorTimeOff.objects
            .filter(
                doctor=doctor,
                is_active=True,
                start_date__lte=appointment_date,
                end_date__gte=appointment_date,
            )
            .exists()
        )

        if has_time_off:
            raise ValidationError({
                "appointment_date":
                    "Doctor is not available on this date."
            })

        # ----------------------------------------------
        # 5. Check Schedule
        # ----------------------------------------------

        weekday = appointment_date.weekday()

        schedule = (
            DoctorSchedule.objects
            .filter(
                doctor=doctor,
                day_of_week=weekday,
                is_active=True,
            )
            .order_by(
                "start_time"
            )
            .first()
        )

        if not schedule:
            raise ValidationError({
                "appointment_date":
                    "Doctor does not work on this day."
            })

        # ----------------------------------------------
        # 6. Check Working Hours
        # ----------------------------------------------

        if not (
            schedule.start_time
            <= appointment_time
            < schedule.end_time
        ):
            raise ValidationError({
                "appointment_time":
                    "Appointment time is outside "
                    "doctor's working hours."
            })

        active_statuses = [
            Appointment.Status.PENDING,
            Appointment.Status.CONFIRMED,
        ]

        # ----------------------------------------------
        # 7. Check Doctor Conflict
        # ----------------------------------------------

        doctor_conflict = (
            Appointment.objects
            .filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=active_statuses,
            )
            .exclude(
                pk=appointment.pk
            )
            .exists()
        )

        if doctor_conflict:
            raise ValidationError({
                "appointment_time":
                    "This time slot is already booked."
            })

        # ----------------------------------------------
        # 8. Check Patient Conflict
        # ----------------------------------------------

        patient_conflict = (
            Appointment.objects
            .filter(
                patient=appointment.patient,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=active_statuses,
            )
            .exclude(
                pk=appointment.pk
            )
            .exists()
        )

        if patient_conflict:
            raise ValidationError({
                "appointment_time":
                    "Patient already has an appointment "
                    "at this time."
            })

        # ----------------------------------------------
        # 9. Update Appointment
        # ----------------------------------------------

        appointment.doctor = doctor

        appointment.doctor_service = (
            doctor_service
        )

        appointment.appointment_date = (
            appointment_date
        )

        appointment.appointment_time = (
            appointment_time
        )

        appointment.notes = notes

        # ----------------------------------------------
        # 10. Save
        # ----------------------------------------------

        try:

            appointment.save(
                update_fields=[
                    "doctor",
                    "doctor_service",
                    "appointment_date",
                    "appointment_time",
                    "notes",
                    "updated_at",
                ]
            )

        except IntegrityError:

            raise ValidationError({
                "appointment_time":
                    "This time slot was just booked "
                    "by another request."
            })

        return appointment

    # ==================================================
    # CANCEL APPOINTMENT
    # ==================================================

    @staticmethod
    @transaction.atomic
    def cancel_appointment(
        *,
        appointment,
    ):

        # ----------------------------------------------
        # 1. Lock Appointment
        # ----------------------------------------------

        appointment = (
            Appointment.objects
            .select_for_update()
            .get(
                pk=appointment.pk
            )
        )

        # ----------------------------------------------
        # 2. Already Cancelled
        # ----------------------------------------------

        if (
            appointment.status
            == Appointment.Status.CANCELLED
        ):
            raise ValidationError({
                "status":
                    "Appointment is already cancelled."
            })

        # ----------------------------------------------
        # 3. Completed
        # ----------------------------------------------

        if (
            appointment.status
            == Appointment.Status.COMPLETED
        ):
            raise ValidationError({
                "status":
                    "Completed appointment cannot "
                    "be cancelled."
            })

        # ----------------------------------------------
        # 4. Cancel
        # ----------------------------------------------

        appointment.status = (
            Appointment.Status.CANCELLED
        )

        appointment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return appointment
