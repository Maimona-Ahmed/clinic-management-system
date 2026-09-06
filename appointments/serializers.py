from rest_framework import serializers

from .models import Appointment

class AppointmentSerializer(
    serializers.ModelSerializer
):

    doctor = serializers.SerializerMethodField()

    service = serializers.SerializerMethodField()

    class Meta:

        model = Appointment

        fields = [
            "id",
            "patient",
            "doctor",
            "doctor_service",
            "service",
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
            "service",
            "status",
            "created_at",
            "updated_at",
        ]

    # ==========================================
    # Doctor
    # ==========================================

    def get_doctor(
        self,
        obj
    ):

        doctor = obj.doctor

        full_name = (
            f"{doctor.user.first_name} "
            f"{doctor.user.last_name}"
        ).strip()

        return {
            "id": doctor.id,
            "name": full_name,
            "specialization": doctor.specialization,
        }

    # ==========================================
    # Service
    # ==========================================

    def get_service(
        self,
        obj
    ):

        doctor_service = obj.doctor_service

        return {
            "id": doctor_service.id,
            "name": doctor_service.service.name,
            "price": doctor_service.price,
            "duration": doctor_service.duration,
        }

    # ==========================================
    # Validation
    # ==========================================

    def validate_doctor_service(
        self,
        value
    ):

        if not value.is_active:

            raise serializers.ValidationError(
                "This doctor service is not active."
            )

        return value

class AppointmentSlotQuerySerializer(serializers.Serializer):

    doctor = serializers.IntegerField()

    service = serializers.IntegerField()

    date = serializers.DateField()

