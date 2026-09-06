from rest_framework import serializers

from appointments.models import Appointment

from .models import (
    MedicalRecord,
    Consultation,
    Diagnosis,
    MedicalNote,
    Prescription,
    PrescriptionItem,
    MedicalTest,
)


# =========================================================
# Medical Record
# =========================================================

class MedicalRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalRecord

        fields = [
            "id",
            "patient",
            "blood_type",
            "allergies",
            "chronic_diseases",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "patient",
            "created_at",
            "updated_at",
        ]


# =========================================================
# Appointment Detail
# =========================================================

class AppointmentDetailSerializer(serializers.ModelSerializer):

    doctor_name = serializers.CharField(
        source="doctor.user.get_full_name",
        read_only=True,
    )

    service_name = serializers.CharField(
        source="doctor_service.service.name",
        read_only=True,
    )

    class Meta:
        model = Appointment

        fields = [
            "id",
            "doctor_name",
            "service_name",
            "appointment_date",
            "appointment_time",
            "status",
        ]

        read_only_fields = fields


# =========================================================
# Diagnosis
# =========================================================

class DiagnosisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diagnosis

        fields = [
            "id",
            "name",
            "description",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Diagnosis name cannot be empty."
            )

        return value


# =========================================================
# Medical Note
# =========================================================

class MedicalNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalNote

        fields = [
            "id",
            "chief_complaint",
            "symptoms",
            "clinical_notes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_chief_complaint(self, value):

        return value.strip()

    def validate_symptoms(self, value):

        return value.strip()

    def validate_clinical_notes(self, value):

        return value.strip()


# =========================================================
# Prescription Item
# =========================================================

class PrescriptionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrescriptionItem

        fields = [
            "id",
            "medicine_name",
            "dosage",
            "frequency",
            "duration",
            "instructions",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_medicine_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Medicine name cannot be empty."
            )

        return value

    def validate_dosage(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Dosage cannot be empty."
            )

        return value

    def validate_frequency(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Frequency cannot be empty."
            )

        return value

    def validate_duration(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Duration cannot be empty."
            )

        return value


# =========================================================
# Prescription
# =========================================================

class PrescriptionSerializer(serializers.ModelSerializer):

    items = PrescriptionItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Prescription

        fields = [
            "id",
            "notes",
            "items",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "items",
            "created_at",
            "updated_at",
        ]

    def validate_notes(self, value):

        return value.strip()


# =========================================================
# Medical Test
# =========================================================

class MedicalTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalTest

        fields = [
            "id",
            "test_name",
            "notes",
            "result",
            "status",
            "requested_at",
            "completed_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "requested_at",
            "completed_at",
        ]

    def validate_test_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Test name cannot be empty."
            )

        return value


# =========================================================
# Medical Record Detail
# =========================================================

class MedicalRecordDetailSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = MedicalRecord

        fields = [
            "id",
            "blood_type",
            "allergies",
            "chronic_diseases",
        ]

        read_only_fields = fields


# =========================================================
# Consultation Detail
# =========================================================

class ConsultationDetailSerializer(
    serializers.ModelSerializer
):

    appointment = AppointmentDetailSerializer(
        read_only=True,
    )

    medical_record = MedicalRecordDetailSerializer(
        read_only=True,
    )

    diagnoses = DiagnosisSerializer(
        many=True,
        read_only=True,
    )

    medical_notes = MedicalNoteSerializer(
        many=True,
        read_only=True,
    )

    prescription = PrescriptionSerializer(
        read_only=True,
    )

    medical_tests = MedicalTestSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Consultation

        fields = [
            "id",
            "appointment",
            "medical_record",
            "status",
            "started_at",
            "completed_at",
            "diagnoses",
            "medical_notes",
            "prescription",
            "medical_tests",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields
