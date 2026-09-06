from django.db import transaction
from django.utils import timezone

from rest_framework.exceptions import ValidationError

from appointments.models import Appointment

from .models import (
    Consultation,
    MedicalRecord,
    Prescription,
)


class ConsultationService:

    # =====================================================
    # Start Consultation
    # =====================================================

    @staticmethod
    @transaction.atomic
    def start_consultation(
        *,
        appointment,
        doctor,
    ):

        # -------------------------------------------------
        # Verify doctor
        # -------------------------------------------------

        if appointment.doctor != doctor:
            raise ValidationError({
                "appointment":
                    "This appointment does not belong "
                    "to the current doctor."
            })

        # -------------------------------------------------
        # Check appointment status
        # -------------------------------------------------

        if appointment.status != Appointment.Status.CONFIRMED:
            raise ValidationError({
                "appointment":
                    "Only confirmed appointments "
                    "can start a consultation."
            })

        # -------------------------------------------------
        # Prevent duplicate consultation
        # -------------------------------------------------

        if Consultation.objects.filter(
            appointment=appointment
        ).exists():

            raise ValidationError({
                "appointment":
                    "Consultation already exists "
                    "for this appointment."
            })

        # -------------------------------------------------
        # Get or create Medical Record
        # -------------------------------------------------

        medical_record, _ = (
            MedicalRecord.objects.get_or_create(
                patient=appointment.patient
            )
        )

        # -------------------------------------------------
        # Create Consultation
        # -------------------------------------------------

        consultation = Consultation.objects.create(
            appointment=appointment,
            medical_record=medical_record,
            status=Consultation.Status.IN_PROGRESS,
            started_at=timezone.now(),
        )

        return consultation

    # =====================================================
    # Complete Consultation
    # =====================================================

    @staticmethod
    @transaction.atomic
    def complete_consultation(
        *,
        consultation,
        doctor,
    ):

        # -------------------------------------------------
        # Verify doctor
        # -------------------------------------------------

        if consultation.appointment.doctor != doctor:
            raise ValidationError({
                "consultation":
                    "This consultation does not "
                    "belong to the current doctor."
            })

        # -------------------------------------------------
        # Check status
        # -------------------------------------------------

        if consultation.status == Consultation.Status.COMPLETED:
            raise ValidationError({
                "status":
                    "Consultation is already completed."
            })

        # -------------------------------------------------
        # Complete consultation
        # -------------------------------------------------

        consultation.status = (
            Consultation.Status.COMPLETED
        )

        consultation.completed_at = timezone.now()

        consultation.save(
            update_fields=[
                "status",
                "completed_at",
                "updated_at",
            ]
        )

        # -------------------------------------------------
        # Complete appointment
        # -------------------------------------------------

        appointment = consultation.appointment

        appointment.status = (
            Appointment.Status.COMPLETED
        )

        appointment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return consultation

    # =====================================================
    # Create Prescription
    # =====================================================

    @staticmethod
    @transaction.atomic
    def create_prescription(
        *,
        consultation,
        notes="",
    ):

        # -------------------------------------------------
        # Check consultation status
        # -------------------------------------------------

        if (
            consultation.status
            != Consultation.Status.IN_PROGRESS
        ):
            raise ValidationError({
                "consultation":
                    "Prescription can only be created "
                    "during an active consultation."
            })

        # -------------------------------------------------
        # Prevent duplicate prescription
        # -------------------------------------------------

        if hasattr(
            consultation,
            "prescription",
        ):
            raise ValidationError({
                "prescription":
                    "Prescription already exists "
                    "for this consultation."
            })

        # -------------------------------------------------
        # Create prescription
        # -------------------------------------------------

        prescription = Prescription.objects.create(
            consultation=consultation,
            notes=notes,
        )

        return prescription
