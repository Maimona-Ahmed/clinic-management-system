
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password
)
from django.db import transaction
from rest_framework import serializers
from appointments.models import Appointment
from .models import DoctorProfile,DoctorSchedule,DoctorTimeOff
from services.models import DoctorService

User = get_user_model()

class DoctorServiceForDoctorSerializer(serializers.ModelSerializer):


    service_name = serializers.CharField(
        source="service.name",
        read_only=True,
    )

    class Meta:
        model = DoctorService

        fields = [
            "id",
            "service",
            "service_name",
            "price",
            "duration",
            "is_active",
        ]


class DoctorSerializer(serializers.ModelSerializer):


    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )
    profile_image = serializers.ImageField(
        read_only =True
    )

    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True,
    )

    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True,
    )

    services = DoctorServiceForDoctorSerializer(
        source="doctor_services",
        many=True,
        read_only=True,
    )

    class Meta:
        model = DoctorProfile

        fields = [
            "id",
            "email",
            "profile_image",
            "first_name",
            "last_name",
            "specialization",
            "license_number",
            "bio",
            "consultation_fee",
            "services",
        ]

        read_only_fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "services",
        ]


class DoctorCreateSerializer( serializers.Serializer):
    email = serializers.EmailField()
    profile_image = serializers.ImageField(
            required=False,
            allow_null=True
        )
    first_name = serializers.CharField(
        max_length=150
    )
    last_name = serializers.CharField(
        max_length=150
    )
    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True
    )
    password = serializers.CharField(
        write_only=True
    )
    specialization = serializers.CharField(
        max_length=100
    )
    license_number = serializers.CharField(
        max_length=50
    )
    bio = serializers.CharField(
        required=False,
        allow_blank=True
    )
    consultation_fee = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    def validate_email(self, value):

        value = value.strip().lower()

        if User.objects.filter(
            email=value
        ).exists():

            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate_password(self, value):

        django_validate_password(value)

        return value

    def validate_license_number(self, value):

        if DoctorProfile.objects.filter(
            license_number=value
        ).exists():

            raise serializers.ValidationError(
                "This license number already exists."
            )

        return value

    @transaction.atomic
    def create(self, validated_data):

        password = validated_data.pop(
            "password"
        )

        user = User.objects.create_user(
            email=validated_data.pop(
                "email"
            ),
            password=password,
            first_name=validated_data.pop(
                "first_name"
            ),
            last_name=validated_data.pop(
                "last_name"
            ),
            phone=validated_data.pop(
                "phone",
                ""
            ),
            role=User.Role.DOCTOR,
        )
        doctor = DoctorProfile.objects.create(
            user=user,
            **validated_data
        )
        return doctor






class DoctorScheduleSerializer(
    serializers.ModelSerializer
):

    day_name = serializers.CharField(
        source="get_day_of_week_display",
        read_only=True,
    )

    class Meta:
        model = DoctorSchedule

        fields = [
            "id",
            "doctor",
            "day_of_week",
            "day_name",
            "start_time",
            "end_time",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "doctor",
            "day_name",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        start_time = attrs.get(
            "start_time"
        )

        end_time = attrs.get(
            "end_time"
        )

        if (
            start_time
            and end_time
            and start_time >= end_time
        ):
            raise serializers.ValidationError({
                "end_time": (
                    "End time must be after "
                    "start time."
                )
            })

        return attrs
    

class DoctorTimeOffSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorTimeOff

        fields = [
            "id",
            "doctor",
            "start_date",
            "end_date",
            "reason",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "doctor",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if (
            start_date
            and end_date
            and end_date < start_date
        ):
            raise serializers.ValidationError({
                "end_date": (
                    "End date must be greater than "
                    "or equal to start date."
                )
            })

        return attrs


class DashboardStatisticsSerializer(
    serializers.Serializer
):

    total_appointments = serializers.IntegerField()

    today_appointments = serializers.IntegerField()

    pending_appointments = serializers.IntegerField()

    confirmed_appointments = serializers.IntegerField()

    completed_appointments = serializers.IntegerField()

    cancelled_appointments = serializers.IntegerField()


class DashboardAppointmentSerializer(
    serializers.ModelSerializer
):

    patient_name = serializers.SerializerMethodField()

    service_name = serializers.CharField(
        source="doctor_service.service.name",
        read_only=True,
    )

    class Meta:
        model = Appointment

        fields = [
            "id",
            "patient_name",
            "service_name",
            "appointment_date",
            "appointment_time",
            "status",
        ]

    def get_patient_name(self, obj):

        return obj.patient.user.get_full_name()




