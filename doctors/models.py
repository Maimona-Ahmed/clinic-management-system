from django.conf import settings
from django.db import models


class DoctorProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
    )

    specialization = models.CharField(
        max_length=100
    )

    license_number = models.CharField(
        max_length=50,
        unique=True
    )

    bio = models.TextField(
        blank=True
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"



class DoctorSchedule(models.Model):

    class WeekDay(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name="schedules",
    )

    day_of_week = models.PositiveSmallIntegerField(
        choices=WeekDay.choices,
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "day_of_week",
            "start_time",
        ]

        indexes = [
            models.Index(
                fields=[
                    "doctor",
                    "day_of_week",
                    "is_active",
                ],
                name="doctor_schedule_day_idx",
            ),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    end_time__gt=models.F(
                        "start_time"
                    )
                ),
                name="schedule_end_after_start",
            ),
        ]

    def __str__(self):
        return (
            f"{self.doctor} - "
            f"{self.get_day_of_week_display()} "
            f"{self.start_time}-{self.end_time}"
        )



class DoctorTimeOff(models.Model):

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name="time_offs",
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.CharField(
        max_length=255,
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

    class Meta:

        indexes = [
            models.Index(
                fields=[
                    "doctor",
                    "start_date",
                    "end_date",
                    "is_active",
                ],
                name="doctor_timeoff_date_idx",
            ),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    end_date__gte=models.F("start_date")
                ),
                name="timeoff_end_after_start",
            ),
        ]

    def __str__(self):
        return (
            f"{self.doctor} - "
            f"{self.start_date} → "
            f"{self.end_date}"
        )
