from datetime import date, time, timedelta
from django.db import IntegrityError

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from doctors.models import (
    DoctorProfile,
    DoctorSchedule,
)
from services.models import DoctorService

from patients.models import PatientProfile

from services.models import Service

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

from .services import ConsultationService


User = get_user_model()


# =========================================================
# Medical Records API Test Case
# =========================================================

class MedicalRecordsAPITestCase(APITestCase):

    def setUp(self):

        # =================================================
        # URLs
        # =================================================

        self.consultation_url = (
            "/api/consultations/"
        )

        self.prescription_item_url = (
            "/api/prescription-items/"
        )

        # =================================================
        # Admin
        # =================================================

        self.admin = (
            User.objects.create_superuser(
                email="admin@example.com",
                password="StrongPassword123!",
            )
        )

        # =================================================
        # Patient 1
        # =================================================

        self.patient_user = (
            User.objects.create_user(
                email="patient@example.com",
                password="StrongPassword123!",
                first_name="Mona",
                last_name="Ali",
                role=User.Role.PATIENT,
            )
        )

        self.patient = (
            PatientProfile.objects.create(
                user=self.patient_user,
            )
        )

        # =================================================
        # Patient 2
        # =================================================

        self.patient2_user = (
            User.objects.create_user(
                email="patient2@example.com",
                password="StrongPassword123!",
                first_name="Sara",
                last_name="Ahmed",
                role=User.Role.PATIENT,
            )
        )

        self.patient2 = (
            PatientProfile.objects.create(
                user=self.patient2_user,
            )
        )

        # =================================================
        # Doctor 1
        # =================================================

        self.doctor_user = (
            User.objects.create_user(
                email="doctor@example.com",
                password="StrongPassword123!",
                first_name="Ahmed",
                last_name="Ali",
                role=User.Role.DOCTOR,
            )
        )

        self.doctor = (
            DoctorProfile.objects.create(
                user=self.doctor_user,
                specialization="Cardiology",
                license_number="DOC-001",
                bio="Heart specialist",
                consultation_fee=50.00,
            )
        )

        # =================================================
        # Doctor 2
        # =================================================

        self.doctor2_user = (
            User.objects.create_user(
                email="doctor2@example.com",
                password="StrongPassword123!",
                first_name="Sara",
                last_name="Ahmed",
                role=User.Role.DOCTOR,
            )
        )

        self.doctor2 = (
            DoctorProfile.objects.create(
                user=self.doctor2_user,
                specialization="Dermatology",
                license_number="DOC-002",
                bio="Skin specialist",
                consultation_fee=60.00,
            )
        )

        # =================================================
        # Services
        # =================================================

        self.service = (
            Service.objects.create(
                name="General Consultation",
                description="General consultation",
            )
        )

        self.service2 = (
            Service.objects.create(
                name="Dermatology Consultation",
                description="Skin consultation",
            )
        )

        # =================================================
        # Doctor Services
        # =================================================

        self.doctor_service = (
            DoctorService.objects.create(
                doctor=self.doctor,
                service=self.service,
                price=50.00,
                duration=30,
                is_active=True,
            )
        )

        self.doctor2_service = (
            DoctorService.objects.create(
                doctor=self.doctor2,
                service=self.service2,
                price=60.00,
                duration=30,
                is_active=True,
            )
        )

        # =================================================
        # Appointment Date
        # =================================================

        today = date.today()

        days_until_monday = (
            7 - today.weekday()
        ) % 7

        if days_until_monday == 0:
            days_until_monday = 7

        self.appointment_date = (
            today
            + timedelta(
                days=days_until_monday
            )
        )

        # =================================================
        # Doctor Schedule
        # =================================================

        self.schedule = (
            DoctorSchedule.objects.create(
                doctor=self.doctor,
                day_of_week=(
                    self.appointment_date.weekday()
                ),
                start_time=time(9, 0),
                end_time=time(14, 0),
                is_active=True,
            )
        )

        # =================================================
        # Doctor 2 Schedule
        # =================================================

        self.schedule2 = (
            DoctorSchedule.objects.create(
                doctor=self.doctor2,
                day_of_week=(
                    self.appointment_date.weekday()
                ),
                start_time=time(9, 0),
                end_time=time(14, 0),
                is_active=True,
            )
        )

        # =================================================
        # Medical Record
        # =================================================

        self.medical_record = (
            MedicalRecord.objects.create(
                patient=self.patient,
                blood_type=(
                    MedicalRecord
                    .BloodType
                    .A_POSITIVE
                ),
                allergies="Penicillin",
                chronic_diseases="Asthma",
            )
        )

        # =================================================
        # Appointment
        # =================================================

        self.appointment = (
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                doctor_service=self.doctor_service,
                appointment_date=(
                    self.appointment_date
                ),
                appointment_time=time(10, 0),
                status=(
                    Appointment
                    .Status
                    .CONFIRMED
                ),
                notes="First visit",
            )
        )

    # =====================================================
    # Helpers
    # =====================================================

    def login_patient(self):

        self.client.force_authenticate(
            user=self.patient_user
        )

    def login_patient2(self):

        self.client.force_authenticate(
            user=self.patient2_user
        )

    def login_doctor(self):

        self.client.force_authenticate(
            user=self.doctor_user
        )

    def login_doctor2(self):

        self.client.force_authenticate(
            user=self.doctor2_user
        )

    # =====================================================
    # Create Appointment Helper
    # =====================================================

    def create_second_appointment(
        self,
        patient=None,
        doctor=None,
        doctor_service=None,
        appointment_time=time(11, 0),
    ):

        if patient is None:
            patient = self.patient2

        if doctor is None:
            doctor = self.doctor2

        if doctor_service is None:
            doctor_service = self.doctor2_service

        return Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            doctor_service=doctor_service,
            appointment_date=(
                self.appointment_date
            ),
            appointment_time=appointment_time,
            status=(
                Appointment
                .Status
                .CONFIRMED
            ),
            notes="Second appointment",
        )

    # =====================================================
    # Start Consultation Helper
    # =====================================================

    def create_consultation(
        self,
        appointment=None,
        doctor=None,
    ):

        if appointment is None:
            appointment = self.appointment

        if doctor is None:
            doctor = self.doctor

        return (
            ConsultationService
            .start_consultation(
                appointment=appointment,
                doctor=doctor,
            )
        )

    # =====================================================
    # CREATE MEDICAL RECORD
    # =====================================================

    def test_medical_record_belongs_to_patient(
        self
    ):

        self.assertEqual(
            self.medical_record.patient,
            self.patient,
        )

        self.assertEqual(
            self.medical_record.blood_type,
            MedicalRecord
            .BloodType
            .A_POSITIVE,
        )

        self.assertEqual(
            self.medical_record.allergies,
            "Penicillin",
        )

        self.assertEqual(
            self.medical_record.chronic_diseases,
            "Asthma",
        )

    # =====================================================
    # MEDICAL RECORD ONE TO ONE
    # =====================================================

    def test_patient_has_one_medical_record(
        self
    ):

        self.assertEqual(
            MedicalRecord.objects.filter(
                patient=self.patient
            ).count(),
            1,
        )

    # =====================================================
    # START CONSULTATION
    # =====================================================

    def test_doctor_can_start_consultation(
        self
    ):

        self.login_doctor()

        url = (
            f"{self.consultation_url}"
            "start/"
        )

        response = self.client.post(
            url,
            {
                "appointment":
                    self.appointment.id
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Consultation.objects.count(),
            1,
        )

        consultation = (
            Consultation.objects.first()
        )

        self.assertEqual(
            consultation.appointment,
            self.appointment,
        )

        self.assertEqual(
            consultation.medical_record.patient,
            self.patient,
        )

        self.assertEqual(
            consultation.status,
            Consultation.Status.IN_PROGRESS,
        )

        self.assertIsNotNone(
            consultation.started_at
        )

    # =====================================================
    # MEDICAL RECORD AUTOMATIC CREATION
    # =====================================================

    def test_start_consultation_uses_patient_medical_record(
        self
    ):

        self.medical_record.delete()

        self.assertFalse(
            MedicalRecord.objects.filter(
                patient=self.patient
            ).exists()
        )

        self.login_doctor()

        response = self.client.post(
            f"{self.consultation_url}start/",
            {
                "appointment":
                    self.appointment.id
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            MedicalRecord.objects.filter(
                patient=self.patient
            ).exists()
        )

        consultation = (
            Consultation.objects.first()
        )

        self.assertEqual(
            consultation.medical_record.patient,
            self.patient,
        )

    # =====================================================
    # PATIENT CANNOT START
    # =====================================================

    def test_patient_cannot_start_consultation(
        self
    ):

        self.login_patient()

        response = self.client.post(
            f"{self.consultation_url}start/",
            {
                "appointment":
                    self.appointment.id
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            Consultation.objects.count(),
            0,
        )

    # =====================================================
    # UNAUTHENTICATED CANNOT START
    # =====================================================

    def test_unauthenticated_cannot_start_consultation(
        self
    ):

        response = self.client.post(
            f"{self.consultation_url}start/",
            {
                "appointment":
                    self.appointment.id
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    # =====================================================
    # WRONG DOCTOR CANNOT START
    # =====================================================

    def test_wrong_doctor_cannot_start_consultation(
        self
    ):

        self.login_doctor2()

        response = self.client.post(
            f"{self.consultation_url}start/",
            {
                "appointment":
                    self.appointment.id
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Consultation.objects.count(),
            0,
        )

    # =====================================================
    # DUPLICATE CONSULTATION
    # =====================================================

    def test_cannot_start_duplicate_consultation(
        self
    ):

        self.create_consultation()

        self.login_doctor()

        response = self.client.post(
            f"{self.consultation_url}start/",
            {
                "appointment":
                    self.appointment.id
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Consultation.objects.count(),
            1,
        )

    # =====================================================
    # WRONG APPOINTMENT STATUS
    # =====================================================

    def test_cannot_start_unconfirmed_appointment(
        self
    ):

        self.appointment.status = (
            Appointment.Status.PENDING
        )

        self.appointment.save(
            update_fields=["status"]
        )

        self.login_doctor()

        response = self.client.post(
            f"{self.consultation_url}start/",
            {
                "appointment":
                    self.appointment.id
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Consultation.objects.count(),
            0,
        )

    # =====================================================
    # CONSULTATION DETAIL
    # =====================================================

    def test_doctor_can_see_own_consultation(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_doctor()

        response = self.client.get(
            f"{self.consultation_url}"
            f"{consultation.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    # =====================================================
    # PATIENT CAN SEE OWN CONSULTATION
    # =====================================================

    def test_patient_can_see_own_consultation(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_patient()

        response = self.client.get(
            f"{self.consultation_url}"
            f"{consultation.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    # =====================================================
    # PATIENT CANNOT SEE OTHER PATIENT
    # =====================================================

    def test_patient_cannot_see_other_patient_consultation(
        self
    ):

        appointment2 = (
            self.create_second_appointment()
        )

        consultation2 = (
            self.create_consultation(
                appointment=appointment2,
                doctor=self.doctor2,
            )
        )

        self.login_patient()

        response = self.client.get(
            f"{self.consultation_url}"
            f"{consultation2.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    # =====================================================
    # DOCTOR CANNOT SEE OTHER DOCTOR
    # =====================================================

    def test_doctor_cannot_see_other_doctor_consultation(
        self
    ):

        appointment2 = (
            self.create_second_appointment()
        )

        consultation2 = (
            self.create_consultation(
                appointment=appointment2,
                doctor=self.doctor2,
            )
        )

        self.login_doctor()

        response = self.client.get(
            f"{self.consultation_url}"
            f"{consultation2.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    # =====================================================
    # PATIENT LIST
    # =====================================================

    def test_patient_can_see_only_own_consultations(
        self
    ):

        consultation1 = (
            self.create_consultation()
        )

        appointment2 = (
            self.create_second_appointment()
        )

        self.create_consultation(
            appointment=appointment2,
            doctor=self.doctor2,
        )

        self.login_patient()

        response = self.client.get(
            self.consultation_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    # =====================================================
    # DOCTOR LIST
    # =====================================================

    def test_doctor_can_see_only_own_consultations(
        self
    ):

        self.create_consultation()

        appointment2 = (
            self.create_second_appointment()
        )

        self.create_consultation(
            appointment=appointment2,
            doctor=self.doctor2,
        )

        self.login_doctor()

        response = self.client.get(
            self.consultation_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    # =====================================================
    # ADD DIAGNOSIS
    # =====================================================

    def test_doctor_can_add_diagnosis(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_doctor()

        url = (
            f"{self.consultation_url}"
            f"{consultation.id}/diagnoses/"
        )

        response = self.client.post(
            url,
            {
                "name": "Influenza",
                "description":
                    "Viral infection",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Diagnosis.objects.count(),
            1,
        )

        diagnosis = (
            Diagnosis.objects.first()
        )

        self.assertEqual(
            diagnosis.consultation,
            consultation,
        )

        self.assertEqual(
            diagnosis.name,
            "Influenza",
        )

    # =====================================================
    # PATIENT CANNOT ADD DIAGNOSIS
    # =====================================================

    def test_patient_cannot_add_diagnosis(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_patient()

        response = self.client.post(
            f"{self.consultation_url}"
            f"{consultation.id}/diagnoses/",
            {
                "name": "Influenza",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            Diagnosis.objects.count(),
            0,
        )

    # =====================================================
    # GET DIAGNOSES
    # =====================================================

    def test_patient_can_see_diagnoses(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        Diagnosis.objects.create(
            consultation=consultation,
            name="Influenza",
            description="Viral infection",
        )

        self.login_patient()

        response = self.client.get(
            f"{self.consultation_url}"
            f"{consultation.id}/diagnoses/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    # =====================================================
    # ADD MEDICAL NOTE
    # =====================================================

    def test_doctor_can_add_medical_note(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_doctor()

        response = self.client.post(
            f"{self.consultation_url}"
            f"{consultation.id}/notes/",
            {
                "chief_complaint":
                    "Headache",

                "symptoms":
                    "Fever and headache",

                "clinical_notes":
                    "Patient appears stable.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            MedicalNote.objects.count(),
            1,
        )

        note = (
            MedicalNote.objects.first()
        )

        self.assertEqual(
            note.consultation,
            consultation,
        )

        self.assertEqual(
            note.chief_complaint,
            "Headache",
        )

    # =====================================================
    # PATIENT CANNOT ADD MEDICAL NOTE
    # =====================================================

    def test_patient_cannot_add_medical_note(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_patient()

        response = self.client.post(
            f"{self.consultation_url}"
            f"{consultation.id}/notes/",
            {
                "chief_complaint":
                    "Headache",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            MedicalNote.objects.count(),
            0,
        )

    # =====================================================
    # CREATE PRESCRIPTION
    # =====================================================

    def test_doctor_can_create_prescription(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_doctor()

        response = self.client.post(
            f"{self.consultation_url}"
            f"{consultation.id}/prescription/",
            {
                "notes":
                    "Take medications regularly.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Prescription.objects.count(),
            1,
        )

        prescription = (
            Prescription.objects.first()
        )

        self.assertEqual(
            prescription.consultation,
            consultation,
        )

        self.assertEqual(
            prescription.notes,
            "Take medications regularly.",
        )

    # =====================================================
    # PATIENT CANNOT CREATE PRESCRIPTION
    # =====================================================

    def test_patient_cannot_create_prescription(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_patient()

        response = self.client.post(
            f"{self.consultation_url}"
            f"{consultation.id}/prescription/",
            {
                "notes":
                    "Prescription",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            Prescription.objects.count(),
            0,
        )

    # =====================================================
    # DUPLICATE PRESCRIPTION
    # =====================================================

    def test_cannot_create_two_prescriptions(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        Prescription.objects.create(
            consultation=consultation,
            notes="First prescription",
        )

        self.login_doctor()

        response = self.client.post(
            f"{self.consultation_url}"
            f"{consultation.id}/prescription/",
            {
                "notes":
                    "Second prescription",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Prescription.objects.count(),
            1,
        )

    # =====================================================
    # GET PRESCRIPTION
    # =====================================================

    def test_patient_can_see_prescription(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        Prescription.objects.create(
            consultation=consultation,
            notes="Take after meals.",
        )

        self.login_patient()

        response = self.client.get(
            f"{self.consultation_url}"
            f"{consultation.id}/prescription/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    # =====================================================
    # CREATE PRESCRIPTION ITEM
    # =====================================================

    def test_doctor_can_create_prescription_item(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        prescription = (
            Prescription.objects.create(
                consultation=consultation,
                notes="Medication",
            )
        )

        self.login_doctor()

        response = self.client.post(
            self.prescription_item_url,
            {
                "prescription":
                    prescription.id,

                "medicine_name":
                    "Paracetamol",

                "dosage":
                    "500 mg",

                "frequency":
                    "3 times daily",

                "duration":
                    "5 days",

                "instructions":
                    "After meals",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            PrescriptionItem.objects.count(),
            1,
        )

        item = (
            PrescriptionItem.objects.first()
        )

        self.assertEqual(
            item.prescription,
            prescription,
        )

        self.assertEqual(
            item.medicine_name,
            "Paracetamol",
        )

    # =====================================================
    # PATIENT CANNOT CREATE ITEM
    # =====================================================

    def test_patient_cannot_create_prescription_item(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        prescription = (
            Prescription.objects.create(
                consultation=consultation,
            )
        )

        self.login_patient()

        response = self.client.post(
            self.prescription_item_url,
            {
                "prescription":
                    prescription.id,

                "medicine_name":
                    "Paracetamol",

                "dosage":
                    "500 mg",

                "frequency":
                    "3 times daily",

                "duration":
                    "5 days",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            PrescriptionItem.objects.count(),
            0,
        )

    # =====================================================
    # PATIENT CAN SEE PRESCRIPTION ITEM
    # =====================================================

    def test_patient_can_see_prescription_item(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        prescription = (
            Prescription.objects.create(
                consultation=consultation,
            )
        )

        item = (
            PrescriptionItem.objects.create(
                prescription=prescription,
                medicine_name="Paracetamol",
                dosage="500 mg",
                frequency="3 times daily",
                duration="5 days",
                instructions="After meals",
            )
        )

        self.login_patient()

        response = self.client.get(
            f"{self.prescription_item_url}"
            f"{item.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    # =====================================================
    # ADD MEDICAL TEST
    # =====================================================

    def test_doctor_can_add_medical_test(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_doctor()

        response = self.client.post(
            f"{self.consultation_url}"
            f"{consultation.id}/tests/",
            {
                "test_name":
                    "CBC",

                "notes":
                    "Complete blood count.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            MedicalTest.objects.count(),
            1,
        )

        medical_test = (
            MedicalTest.objects.first()
        )

        self.assertEqual(
            medical_test.consultation,
            consultation,
        )

        self.assertEqual(
            medical_test.test_name,
            "CBC",
        )

        self.assertEqual(
            medical_test.status,
            MedicalTest.Status.REQUESTED,
        )

    # =====================================================
    # PATIENT CANNOT ADD MEDICAL TEST
    # =====================================================

    def test_patient_cannot_add_medical_test(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_patient()

        response = self.client.post(
            f"{self.consultation_url}"
            f"{consultation.id}/tests/",
            {
                "test_name":
                    "CBC",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            MedicalTest.objects.count(),
            0,
        )

    # =====================================================
    # GET MEDICAL TESTS
    # =====================================================

    def test_patient_can_see_medical_tests(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        MedicalTest.objects.create(
            consultation=consultation,
            test_name="CBC",
            notes="Blood test",
        )

        self.login_patient()

        response = self.client.get(
            f"{self.consultation_url}"
            f"{consultation.id}/tests/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    # =====================================================
    # MEDICAL TEST DEFAULT STATUS
    # =====================================================

    def test_medical_test_default_status(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        medical_test = (
            MedicalTest.objects.create(
                consultation=consultation,
                test_name="CBC",
            )
        )

        self.assertEqual(
            medical_test.status,
            MedicalTest.Status.REQUESTED,
        )

        self.assertIsNone(
            medical_test.completed_at
        )

    # =====================================================
    # COMPLETE CONSULTATION
    # =====================================================

    def test_doctor_can_complete_consultation(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_doctor()

        response = self.client.post(
            f"{self.consultation_url}"
            f"{consultation.id}/complete/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        consultation.refresh_from_db()

        self.assertEqual(
            consultation.status,
            Consultation.Status.COMPLETED,
        )

        self.assertIsNotNone(
            consultation.completed_at
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.COMPLETED,
        )

    # =====================================================
    # PATIENT CANNOT COMPLETE
    # =====================================================

    def test_patient_cannot_complete_consultation(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_patient()

        response = self.client.post(
            f"{self.consultation_url}"
            f"{consultation.id}/complete/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        consultation.refresh_from_db()

        self.assertEqual(
            consultation.status,
            Consultation.Status.IN_PROGRESS,
        )

    # =====================================================
    # WRONG DOCTOR CANNOT COMPLETE
    # =====================================================

    def test_wrong_doctor_cannot_complete_consultation(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        self.login_doctor2()

        response = self.client.post(
            f"{self.consultation_url}"
            f"{consultation.id}/complete/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        consultation.refresh_from_db()

        self.assertEqual(
            consultation.status,
            Consultation.Status.IN_PROGRESS,
        )

    # =====================================================
    # COMPLETE CONSULTATION SERVICE
    # =====================================================

    def test_complete_consultation_service(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        consultation = (
            ConsultationService
            .complete_consultation(
                consultation=consultation,
                doctor=self.doctor,
            )
        )

        self.assertEqual(
            consultation.status,
            Consultation.Status.COMPLETED,
        )

        self.assertIsNotNone(
            consultation.completed_at
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.Status.COMPLETED,
        )

    # =====================================================
    # CANNOT COMPLETE TWICE
    # =====================================================

    def test_cannot_complete_consultation_twice(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        ConsultationService.complete_consultation(
            consultation=consultation,
            doctor=self.doctor,
        )

        with self.assertRaises(
            ValidationError
        ):

            ConsultationService.complete_consultation(
                consultation=consultation,
                doctor=self.doctor,
            )

    # =====================================================
    # CANNOT CREATE PRESCRIPTION AFTER COMPLETE
    # =====================================================

    def test_cannot_create_prescription_after_complete(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        ConsultationService.complete_consultation(
            consultation=consultation,
            doctor=self.doctor,
        )

        with self.assertRaises(
            ValidationError
        ):

            ConsultationService.create_prescription(
                consultation=consultation,
                notes="Late prescription",
            )

    # =====================================================
    # COMPLETED CONSULTATION HAS DATE
    # =====================================================

    def test_completed_consultation_has_completed_at(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        ConsultationService.complete_consultation(
            consultation=consultation,
            doctor=self.doctor,
        )

        consultation.refresh_from_db()

        self.assertEqual(
            consultation.status,
            Consultation.Status.COMPLETED,
        )

        self.assertIsNotNone(
            consultation.completed_at
        )

    # =====================================================
    # MEDICAL TEST COMPLETED CONSTRAINT
    # =====================================================

    def test_completed_medical_test_requires_date(self):

        consultation = self.create_consultation()

        with self.assertRaises(IntegrityError):

            MedicalTest.objects.create(
                consultation=consultation,
                test_name="CBC",
                status=MedicalTest.Status.COMPLETED,
                completed_at=None,
            )


    # =====================================================
    # MEDICAL TEST COMPLETION
    # =====================================================

    def test_completed_medical_test_can_have_date(
        self
    ):

        from django.utils import timezone

        consultation = (
            self.create_consultation()
        )

        medical_test = (
            MedicalTest.objects.create(
                consultation=consultation,
                test_name="CBC",
                status=(
                    MedicalTest
                    .Status
                    .COMPLETED
                ),
                completed_at=timezone.now(),
            )
        )

        medical_test.full_clean()

        self.assertEqual(
            medical_test.status,
            MedicalTest.Status.COMPLETED,
        )

        self.assertIsNotNone(
            medical_test.completed_at
        )

    # =====================================================
    # CONSULTATION COMPLETION CONSTRAINT
    # =====================================================

    def test_completed_consultation_requires_date(
        self
    ):

        consultation = (
            self.create_consultation()
        )

        consultation.status = (
            Consultation
            .Status
            .COMPLETED
        )

        consultation.completed_at = None

        with self.assertRaises(Exception):

            consultation.full_clean()

    # =====================================================
    # CONSULTATION COMPLETION VALID
    # =====================================================

    def test_completed_consultation_with_date_is_valid(
        self
    ):

        from django.utils import timezone

        consultation = (
            self.create_consultation()
        )

        consultation.status = (
            Consultation
            .Status
            .COMPLETED
        )

        consultation.completed_at = (
            timezone.now()
        )

        consultation.full_clean()

        self.assertEqual(
            consultation.status,
            Consultation.Status.COMPLETED,
        )

        self.assertIsNotNone(
            consultation.completed_at
        )
