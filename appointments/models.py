from django.db import models
from django.conf import settings

class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    patient = models.ForeignKey(
        "patients.PatientProfile",
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    doctor = models.ForeignKey(
        "doctors.DoctorProfile",
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    doctor_service = models.ForeignKey(
        "services.DoctorService",
        on_delete=models.PROTECT,
        related_name="appointments",
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-appointment_date",
            "-appointment_time",
        ]

        indexes = [
            models.Index(
                fields=[
                    "doctor",
                    "appointment_date",
                    "appointment_time",
                ],
                name="appointment_doctor_slot_idx",
            ),
            models.Index(
                fields=[
                    "patient",
                    "appointment_date",
                    "appointment_time",
                ],
                name="appointment_patient_slot_idx",
            ),
            models.Index(
                fields=[
                    "status",
                    "appointment_date",
                ],
                name="appointment_status_date_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "doctor",
                    "appointment_date",
                    "appointment_time",
                ],
                condition=models.Q(
                    status__in=[
                        "PENDING",
                        "CONFIRMED",
                    ]
                ),
                name="unique_active_doctor_slot",
            ),

            models.CheckConstraint(
                condition=models.Q(
                    appointment_date__isnull=False
                ),
                name="appointment_date_required",
            ),
        ]

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.doctor} - "
            f"{self.appointment_date} "
            f"{self.appointment_time}"
        )
