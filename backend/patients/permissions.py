
from rest_framework.permissions import BasePermission


class IsAdminOrSelf(BasePermission):

    message = (
        "You can only access your own patient profile."
    )

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
        )

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):

        if request.user.is_staff:
            return True

        return obj.user == request.user
