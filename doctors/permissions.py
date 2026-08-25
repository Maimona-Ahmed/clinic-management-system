
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):

    message = "Only administrators can manage doctors."

    def has_permission(
        self,
        request,
        view
    ):
        return (
            request.user.is_authenticated
            and request.user.is_staff
        )
    

class DoctorSchedulePermission(
    BasePermission
):

    def has_permission(
        self,
        request,
        view,
    ):

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if hasattr(
            request.user,
            "doctor_profile",
        ):
            return True

        return False

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        if request.user.is_superuser:
            return True

        if hasattr(
            request.user,
            "doctor_profile",
        ):
            return (
                obj.doctor
                == request.user.doctor_profile
            )

        return False




