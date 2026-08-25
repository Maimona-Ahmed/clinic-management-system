from rest_framework.permissions import (
    BasePermission,
)


class ConsultationPermission(BasePermission):

    """
    Controls access to consultations.

    Doctor:
        - Can see his consultations.
        - Can start consultations.
        - Can complete consultations.
        - Can add diagnoses, notes, prescriptions and tests.

    Patient:
        - Can see his own consultations.
        - Cannot start or complete consultations.
        - Cannot modify medical information.
    """

    def has_permission(
        self,
        request,
        view,
    ):

        user = request.user

        # -------------------------------------------------
        # Authentication
        # -------------------------------------------------

        if not user.is_authenticated:
            return False

        # -------------------------------------------------
        # Start consultation
        # -------------------------------------------------

        if view.action == "start":
            return hasattr(
                user,
                "doctor_profile",
            )

        # -------------------------------------------------
        # Complete consultation
        # -------------------------------------------------

        if view.action == "complete":
            return hasattr(
                user,
                "doctor_profile",
            )

        # -------------------------------------------------
        # Write medical data
        # -------------------------------------------------

        if request.method in [
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        ]:

            return hasattr(
                user,
                "doctor_profile",
            )

        # -------------------------------------------------
        # GET
        # -------------------------------------------------

        return (
            hasattr(
                user,
                "doctor_profile",
            )
            or
            hasattr(
                user,
                "patient_profile",
            )
        )

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        user = request.user

        # -------------------------------------------------
        # Doctor
        # -------------------------------------------------

        if hasattr(
            user,
            "doctor_profile",
        ):

            return (
                obj.appointment.doctor
                == user.doctor_profile
            )

        # -------------------------------------------------
        # Patient
        # -------------------------------------------------

        if hasattr(
            user,
            "patient_profile",
        ):

            return (
                obj.appointment.patient
                == user.patient_profile
            )

        return False


class PrescriptionItemPermission(
    BasePermission
):

    """
    Controls access to prescription items.
    """

    def has_permission(
        self,
        request,
        view,
    ):

        user = request.user

        if not user.is_authenticated:
            return False

        # Doctor can manage items.
        if hasattr(
            user,
            "doctor_profile",
        ):
            return True

        # Patient can only read.
        if (
            hasattr(
                user,
                "patient_profile",
            )
            and request.method == "GET"
        ):
            return True

        return False

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        consultation = (
            obj.prescription.consultation
        )

        user = request.user

        # -------------------------------------------------
        # Doctor
        # -------------------------------------------------

        if hasattr(
            user,
            "doctor_profile",
        ):

            return (
                consultation
                .appointment
                .doctor
                == user.doctor_profile
            )

        # -------------------------------------------------
        # Patient
        # -------------------------------------------------

        if hasattr(
            user,
            "patient_profile",
        ):

            return (
                consultation
                .appointment
                .patient
                == user.patient_profile
            )

        return False
