from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


# =========================================================
# Medical Record
# =========================================================

class MedicalRecord(models.Model):

    class BloodType(models.TextChoices):
        A_POSITIVE = "A+", "A+"
        A_NEGATIVE = "A-", "A-"
        B_POSITIVE = "B+", "B+"
        B_NEGATIVE = "B-", "B-"
        AB_POSITIVE = "AB+", "AB+"
        AB_NEGATIVE = "AB-", "AB-"
        O_POSITIVE = "O+", "O+"
        O_NEGATIVE = "O-", "O-"
        UNKNOWN = "UNKNOWN", "Unknown"

    patient = models.OneToOneField(
        "patients.PatientProfile",
        on_delete=models.CASCADE,
        related_name="medical_record",
    )

    blood_type = models.CharField(
        max_length=10,
        choices=BloodType.choices,
        default=BloodType.UNKNOWN,
    )

    allergies = models.TextField(
        blank=True,
    )

    chronic_diseases = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["blood_type"],
                name="medical_record_blood_idx",
            ),
        ]

    def __str__(self):
        return f"Medical Record - {self.patient}"


# =========================================================
# Consultation
# =========================================================

class Consultation(models.Model):

    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    appointment = models.OneToOneField(
        "appointments.Appointment",
        on_delete=models.PROTECT,
        related_name="consultation",
    )

    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.PROTECT,
        related_name="consultations",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
    )

    started_at = models.DateTimeField(
        auto_now_add=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "medical_record",
                    "status",
                ],
                name="consult_record_status_idx",
            ),
            models.Index(
                fields=[
                    "status",
                    "started_at",
                ],
                name="consult_status_started_idx",
            ),
        ]

        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(
                        status="COMPLETED",
                        completed_at__isnull=False,
                    )
                    |
                    ~models.Q(
                        status="COMPLETED"
                    )
                ),
                name="completed_consultation_has_date",
            ),
        ]

    def __str__(self):
        return (
            f"Consultation #{self.id} - "
            f"{self.appointment}"
        )


# =========================================================
# Diagnosis
# =========================================================

class Diagnosis(models.Model):

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name="diagnoses",
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["id"]

        indexes = [
            models.Index(
                fields=[
                    "consultation",
                ],
                name="diagnosis_consult_idx",
            ),
            models.Index(
                fields=[
                    "name",
                ],
                name="diagnosis_name_idx",
            ),
        ]

    def __str__(self):
        return self.name


# =========================================================
# Medical Note
# =========================================================

class MedicalNote(models.Model):

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name="medical_notes",
    )

    chief_complaint = models.TextField(
        blank=True,
    )

    symptoms = models.TextField(
        blank=True,
    )

    clinical_notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "consultation",
                ],
                name="medical_note_consult_idx",
            ),
        ]

    def __str__(self):
        return (
            f"Medical Note - "
            f"Consultation #{self.consultation_id}"
        )


# =========================================================
# Prescription
# =========================================================

class Prescription(models.Model):

    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name="prescription",
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

    def __str__(self):
        return (
            f"Prescription - "
            f"Consultation #{self.consultation_id}"
        )


# =========================================================
# Prescription Item
# =========================================================

class PrescriptionItem(models.Model):

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="items",
    )

    medicine_name = models.CharField(
        max_length=255,
    )

    dosage = models.CharField(
        max_length=100,
    )

    frequency = models.CharField(
        max_length=100,
    )

    duration = models.CharField(
        max_length=100,
    )

    instructions = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["id"]

        indexes = [
            models.Index(
                fields=[
                    "prescription",
                ],
                name="prescription_item_idx",
            ),
            models.Index(
                fields=[
                    "medicine_name",
                ],
                name="prescription_medicine_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.medicine_name} - "
            f"{self.dosage}"
        )


# =========================================================
# Medical Test
# =========================================================

class MedicalTest(models.Model):

    class Status(models.TextChoices):
        REQUESTED = "REQUESTED", "Requested"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name="medical_tests",
    )

    test_name = models.CharField(
        max_length=255,
    )

    notes = models.TextField(
        blank=True,
    )

    result = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REQUESTED,
    )

    requested_at = models.DateTimeField(
        auto_now_add=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-requested_at"]

        indexes = [
            models.Index(
                fields=[
                    "consultation",
                    "status",
                ],
                name="med_test_cons_status_idx",
            ),
            models.Index(
                fields=[
                    "status",
                ],
                name="medical_test_status_idx",
            ),
        ]

        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(
                        status="COMPLETED",
                        completed_at__isnull=False,
                    )
                    |
                    ~models.Q(
                        status="COMPLETED"
                    )
                ),
                name="completed_test_has_date",
            ),
        ]

    def __str__(self):
        return self.test_name
