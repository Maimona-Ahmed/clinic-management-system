from django.contrib import admin

from .models import (
    User,
    ReceptionistProfile,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
    )


# @admin.register(PatientProfile)
# class PatientProfileAdmin(admin.ModelAdmin):

#     list_display = (
#         "user",
#         "date_of_birth",
#         "gender",
#     )

#     search_fields = (
#         "user__email",
#         "user__first_name",
#         "user__last_name",
#     )


# @admin.register(DoctorProfile)
# class DoctorProfileAdmin(admin.ModelAdmin):

#     list_display = (
#         "user",
#         "specialization",
#         "license_number",
#         "consultation_fee",
#     )

#     list_filter = (
#         "specialization",
#     )

#     search_fields = (
#         "user__email",
#         "user__first_name",
#         "user__last_name",
#         "license_number",
#     )


@admin.register(ReceptionistProfile)
class ReceptionistProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "employee_id",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "employee_id",
    )
