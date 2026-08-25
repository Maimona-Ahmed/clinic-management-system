from rest_framework import serializers
from .models import Service, DoctorService


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service

        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class DoctorServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorService

        fields = [
            "id",
            "doctor",
            "service",
            "price",
            "duration",
            "is_active",
        ]

        read_only_fields = [
            "id",
        ]


class ServiceDoctorSerializer(serializers.ModelSerializer):

    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = DoctorService

        fields = [
            "doctor",
            "doctor_name",
            "price",
            "duration",
            "is_active",
        ]

    def get_doctor_name(self, obj):
        return obj.doctor.user.get_full_name()


class ServiceDetailSerializer(serializers.ModelSerializer):

    doctors = ServiceDoctorSerializer(
        source="doctor_services",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Service

        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "doctors",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "doctors",
            "created_at",
            "updated_at",
        ]
