from rest_framework.permissions import (
    BasePermission,
)


class InvoicePermission(
    BasePermission
):

    def has_permission(
        self,
        request,
        view,
    ):

        user = request.user

        if not user.is_authenticated:
            return False

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

        # ----------------------------------------------
        # Patient
        # ----------------------------------------------

        if hasattr(
            user,
            "patient_profile",
        ):

            return (
                obj.appointment.patient
                == user.patient_profile
            )

        # ----------------------------------------------
        # Doctor
        # ----------------------------------------------

        if hasattr(
            user,
            "doctor_profile",
        ):

            return (
                obj.appointment.doctor
                == user.doctor_profile
            )

        return False


class PaymentPermission(
    BasePermission
):

    def has_permission(
        self,
        request,
        view,
    ):

        user = request.user

        if not user.is_authenticated:
            return False

        # Reading payments
        if request.method in [
            "GET",
        ]:

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

        # Creating payment
        # Later we can replace this with
        # cashier/admin permission.

        if request.method == "POST":

            return (
                hasattr(
                    user,
                    "patient_profile",
                )
            )

        return False

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        user = request.user

        # ----------------------------------------------
        # Patient
        # ----------------------------------------------

        if hasattr(
            user,
            "patient_profile",
        ):

            return (
                obj.invoice
                .appointment
                .patient
                == user.patient_profile
            )

        # ----------------------------------------------
        # Doctor
        # ----------------------------------------------

        if hasattr(
            user,
            "doctor_profile",
        ):

            return (
                obj.invoice
                .appointment
                .doctor
                == user.doctor_profile
            )

        return False
