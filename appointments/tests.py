from datetime import date, time, timedelta

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from doctors.models import (
    DoctorProfile,
    DoctorSchedule,
    DoctorTimeOff,
)
from services.models import DoctorService
from patients.models import PatientProfile

from services.models import Service

from .models import Appointment


User = get_user_model()


class AppointmentAPITestCase(APITestCase):

    def setUp(self):

        self.appointment_url = (
            "/api/appointments/"
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
        # Service
        # =================================================

        self.service = (
            Service.objects.create(
                name="General Consultation",
                description="General consultation",
            )
        )

        self.service2 = (
            Service.objects.create(
                name="ECG",
                description="Electrocardiogram",
            )
        )

        # =================================================
        # Doctor Service
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
        #
        # Find next Monday
        #

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

    # =====================================================
    # Helper
    # =====================================================

    def appointment_payload(
        self,
        doctor_service=None,
        appointment_time="10:00:00",
    ):

        if doctor_service is None:
            doctor_service = (
                self.doctor_service
            )

        return {
            "doctor_service": (
                doctor_service.id
            ),
            "appointment_date": str(
                self.appointment_date
            ),
            "appointment_time": (
                appointment_time
            ),
            "notes": "First visit",
        }

    # =====================================================
    # CREATE
    # =====================================================

    def test_patient_can_create_appointment(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.appointment_url,
            self.appointment_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Appointment.objects.count(),
            1,
        )

        appointment = (
            Appointment.objects.first()
        )

        self.assertEqual(
            appointment.patient,
            self.patient,
        )

        self.assertEqual(
            appointment.doctor,
            self.doctor,
        )

        self.assertEqual(
            appointment.doctor_service,
            self.doctor_service,
        )

        self.assertEqual(
            appointment.status,
            Appointment.Status.PENDING,
        )

    # =====================================================
    # DOCTOR CANNOT CREATE
    # =====================================================

    def test_doctor_cannot_create_appointment(
        self
    ):

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.post(
            self.appointment_url,
            self.appointment_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            Appointment.objects.count(),
            0,
        )

    # =====================================================
    # UNAUTHENTICATED
    # =====================================================

    def test_unauthenticated_user_cannot_create_appointment(
        self
    ):

        response = self.client.post(
            self.appointment_url,
            self.appointment_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    # =====================================================
    # LIST - PATIENT OWNERSHIP
    # =====================================================

    def test_patient_can_see_only_own_appointments(
        self
    ):

        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            doctor_service=self.doctor_service,
            appointment_date=self.appointment_date,
            appointment_time=time(10, 0),
            status=Appointment.Status.PENDING,
        )

        Appointment.objects.create(
            patient=self.patient2,
            doctor=self.doctor,
            doctor_service=self.doctor_service,
            appointment_date=self.appointment_date,
            appointment_time=time(11, 0),
            status=Appointment.Status.PENDING,
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            self.appointment_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["patient"],
            self.patient.id,
        )

    # =====================================================
    # DETAIL OWNERSHIP
    # =====================================================

    def test_patient_cannot_access_another_patient_appointment(
        self
    ):

        appointment = (
            Appointment.objects.create(
                patient=self.patient2,
                doctor=self.doctor,
                doctor_service=self.doctor_service,
                appointment_date=self.appointment_date,
                appointment_time=time(10, 0),
                status=Appointment.Status.PENDING,
            )
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            f"{self.appointment_url}"
            f"{appointment.id}/"
        )

        # Because get_queryset() only returns
        # the current patient's appointments,
        # DRF returns 404.
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    # =====================================================
    # DOCTOR LIST
    # =====================================================

    def test_doctor_can_see_own_appointments(
        self
    ):

        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            doctor_service=self.doctor_service,
            appointment_date=self.appointment_date,
            appointment_time=time(10, 0),
            status=Appointment.Status.PENDING,
        )

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.get(
            self.appointment_url
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
    # INACTIVE DOCTOR SERVICE
    # =====================================================

    def test_cannot_book_inactive_doctor_service(
        self
    ):

        self.doctor_service.is_active = False

        self.doctor_service.save(
            update_fields=["is_active"]
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.appointment_url,
            self.appointment_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Appointment.objects.count(),
            0,
        )

    # =====================================================
    # TIME OFF
    # =====================================================

    def test_cannot_book_doctor_time_off(
        self
    ):

        DoctorTimeOff.objects.create(
            doctor=self.doctor,
            start_date=self.appointment_date,
            end_date=self.appointment_date,
            reason="Vacation",
            is_active=True,
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.appointment_url,
            self.appointment_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Appointment.objects.count(),
            0,
        )

    # =====================================================
    # NON WORKING DAY
    # =====================================================

    def test_cannot_book_on_non_working_day(
        self
    ):

        # Remove the only schedule
        self.schedule.delete()

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.appointment_url,
            self.appointment_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Appointment.objects.count(),
            0,
        )

    # =====================================================
    # OUTSIDE WORKING HOURS
    # =====================================================

    def test_cannot_book_outside_working_hours(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.appointment_url,
            self.appointment_payload(
                appointment_time="15:00:00"
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Appointment.objects.count(),
            0,
        )

    # =====================================================
    # DOCTOR SLOT CONFLICT
    # =====================================================

    def test_cannot_book_existing_doctor_slot(
        self
    ):

        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            doctor_service=self.doctor_service,
            appointment_date=self.appointment_date,
            appointment_time=time(10, 0),
            status=Appointment.Status.PENDING,
        )

        self.client.force_authenticate(
            user=self.patient2_user
        )

        response = self.client.post(
            self.appointment_url,
            self.appointment_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Appointment.objects.count(),
            1,
        )

    # =====================================================
    # PATIENT CONFLICT
    # =====================================================

    def test_patient_cannot_have_two_appointments_same_time(
        self
    ):

        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            doctor_service=self.doctor_service,
            appointment_date=self.appointment_date,
            appointment_time=time(10, 0),
            status=Appointment.Status.PENDING,
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.appointment_url,
            self.appointment_payload(
                doctor_service=self.doctor2_service
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Appointment.objects.count(),
            1,
        )

    # =====================================================
    # RETRIEVE OWN APPOINTMENT
    # =====================================================

    def test_patient_can_retrieve_own_appointment(
        self
    ):

        appointment = (
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                doctor_service=self.doctor_service,
                appointment_date=self.appointment_date,
                appointment_time=time(10, 0),
                status=Appointment.Status.PENDING,
            )
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            f"{self.appointment_url}"
            f"{appointment.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            appointment.id,
        )

    # =====================================================
    # PATIENT CANNOT UPDATE
    # =====================================================

    def test_patient_cannot_update_appointment(
        self
    ):

        appointment = (
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                doctor_service=self.doctor_service,
                appointment_date=self.appointment_date,
                appointment_time=time(10, 0),
                status=Appointment.Status.PENDING,
            )
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.patch(
            f"{self.appointment_url}"
            f"{appointment.id}/",
            {
                "notes": "Changed",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # =====================================================
    # PATIENT CANNOT DELETE
    # =====================================================

    def test_patient_cannot_delete_appointment(
        self
    ):

        appointment = (
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                doctor_service=self.doctor_service,
                appointment_date=self.appointment_date,
                appointment_time=time(10, 0),
                status=Appointment.Status.PENDING,
            )
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.delete(
            f"{self.appointment_url}"
            f"{appointment.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            Appointment.objects.filter(
                id=appointment.id
            ).exists()
        )

    # =====================================================
    # CANCEL
    # =====================================================

    def test_patient_can_cancel_appointment(
        self
    ):

        appointment = (
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                doctor_service=self.doctor_service,
                appointment_date=self.appointment_date,
                appointment_time=time(10, 0),
                status=Appointment.Status.PENDING,
            )
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            f"{self.appointment_url}"
            f"{appointment.id}/cancel/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            Appointment.Status.CANCELLED,
        )

    # =====================================================
    # CANNOT CANCEL COMPLETED
    # =====================================================

    def test_completed_appointment_cannot_be_cancelled(
        self
    ):

        appointment = (
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                doctor_service=self.doctor_service,
                appointment_date=self.appointment_date,
                appointment_time=time(10, 0),
                status=Appointment.Status.COMPLETED,
            )
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            f"{self.appointment_url}"
            f"{appointment.id}/cancel/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            Appointment.Status.COMPLETED,
        )

    # =====================================================
    # ALREADY CANCELLED
    # =====================================================

    def test_already_cancelled_appointment(
        self
    ):

        appointment = (
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                doctor_service=self.doctor_service,
                appointment_date=self.appointment_date,
                appointment_time=time(10, 0),
                status=Appointment.Status.CANCELLED,
            )
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            f"{self.appointment_url}"
            f"{appointment.id}/cancel/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            Appointment.Status.CANCELLED,
        )
