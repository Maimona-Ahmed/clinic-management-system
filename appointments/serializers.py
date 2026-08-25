from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Appointment

        fields = [
            "id",
            "patient",
            "doctor",
            "doctor_service",
            "appointment_date",
            "appointment_time",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "patient",
            "doctor",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_doctor_service(
        self,
        value,
    ):

        if not value.is_active:
            raise serializers.ValidationError(
                "This doctor service is not active."
            )

        return value
