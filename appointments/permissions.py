from rest_framework.permissions import BasePermission


class AppointmentPermission(
    BasePermission
):

    def has_permission(
        self,
        request,
        view,
    ):

        user = request.user

        # ------------------------------------------
        # Create
        # ------------------------------------------

        if view.action == "create":

            return hasattr(
                user,
                "patient_profile",
            )

        # ------------------------------------------
        # Other actions
        # ------------------------------------------

        return (
            hasattr(
                user,
                "patient_profile",
            )
            or
            hasattr(
                user,
                "doctor_profile",
            )
        )

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        user = request.user

        # ==========================================
        # Patient
        # ==========================================

        if hasattr(
            user,
            "patient_profile",
        ):

            if obj.patient != user.patient_profile:
                return False

            if view.action in [
                "retrieve",
                "list",
                "cancel",
            ]:
                return True

            return False

        # ==========================================
        # Doctor
        # ==========================================

        if hasattr(
            user,
            "doctor_profile",
        ):

            if obj.doctor != user.doctor_profile:
                return False

            if view.action in [
                "retrieve",
                "list",
                "cancel",
                "confirm"
            ]:
                return True

            return False

        return False
