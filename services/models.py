from django.db import models

class Service(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name


class DoctorService(models.Model):
    doctor = models.ForeignKey(
        "doctors.DoctorProfile",
        on_delete=models.CASCADE,
        related_name="doctor_services",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="doctor_services",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in minutes",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "service"],
                name="unique_doctor_service",
            ),
        ]

    def __str__(self):
        return f"{self.doctor} - {self.service}"
