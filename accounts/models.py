from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"
        RECEPTIONIST = "RECEPTIONIST", "Receptionist"
        ADMIN = "ADMIN", "Admin"

    username = None

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
    
# class PatientProfile(models.Model):

#     class Gender(models.TextChoices):
#         MALE = "M", "Male"
#         FEMALE = "F", "Female"

#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name="patient_profile"
#     )

#     date_of_birth = models.DateField(
#         null=True,
#         blank=True
#     )

#     gender = models.CharField(
#         max_length=1,
#         choices=Gender.choices,
#         blank=True
#     )

#     address = models.TextField(
#         blank=True
#     )

#     emergency_contact = models.CharField(
#         max_length=20,
#         blank=True
#     )

#     def __str__(self):
#         return f"Patient: {self.user.get_full_name()}"
    
# class DoctorProfile(models.Model):

#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name="doctor_profile"
#     )

#     specialization = models.CharField(
#         max_length=100
#     )

#     license_number = models.CharField(
#         max_length=50,
#         unique=True
#     )

#     bio = models.TextField(
#         blank=True
#     )

#     consultation_fee = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )

#     def __str__(self):
#         return f"Dr. {self.user.get_full_name()}"

class ReceptionistProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="receptionist_profile"
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return (
            f"Receptionist: "
            f"{self.user.get_full_name()}"
        )


