from django.contrib import admin
from .models import DoctorProfile

@admin.register(DoctorProfile)
class DoctorProfileAdmin(
    admin.ModelAdmin
):

    list_display = (
        "user",
        "specialization",
        "license_number",
        "consultation_fee",
    )

    list_filter = (
        "specialization",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "license_number",
    )
