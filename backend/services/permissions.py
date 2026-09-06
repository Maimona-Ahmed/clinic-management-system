from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission


User = get_user_model()


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )


class IsAdminOrDoctorOwner(
    BasePermission
):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return (
            request.user.is_superuser
            or request.user.role == User.Role.DOCTOR
        )

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        if request.user.is_superuser:
            return True

        return obj.doctor.user == request.user
