
from rest_framework import serializers

from .models import PatientProfile


class PatientSerializer(
    serializers.ModelSerializer
):

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True
    )

    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True
    )

    phone = serializers.CharField(
        source="user.phone",
        read_only=True
    )

    class Meta:

        model = PatientProfile

        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "date_of_birth",
            "gender",
            "blood_type",
            "address",
            "emergency_contact_name",
            "emergency_contact_phone",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "created_at",
            "updated_at",
        ]
