from decimal import Decimal

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from doctors.models import DoctorProfile

from .models import (
    Service,
    DoctorService,
)


User = get_user_model()


class ServiceAPITestCase(
    APITestCase
):

    def setUp(self):

        self.service_url = (
            "/api/services/"
        )

        self.doctor_service_url = (
            "/api/doctor-services/"
        )


        self.admin = (
            User.objects.create_superuser(
                email="admin@example.com",
                password="StrongPassword123!",
            )
        )

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
                specialization="Dentistry",
                license_number="DOC-002",
                bio="Dentist",
                consultation_fee=40.00,
            )
        )


        self.patient = (
            User.objects.create_user(
                email="patient@example.com",
                password="StrongPassword123!",
                first_name="Mona",
                last_name="Ali",
                role=User.Role.PATIENT,
            )
        )


        self.receptionist = (
            User.objects.create_user(
                email="reception@example.com",
                password="StrongPassword123!",
                first_name="Reception",
                last_name="User",
                role=User.Role.RECEPTIONIST,
            )
        )


        self.service = (
            Service.objects.create(
                name="Cardiology",
                description=(
                    "Heart consultation"
                ),
            )
        )

        self.service2 = (
            Service.objects.create(
                name="ECG",
                description=(
                    "Electrocardiogram"
                ),
            )
        )

    def test_anyone_can_list_services(self):

        response = self.client.get(
            self.service_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )
    def test_anyone_can_retrieve_service(self):

        response = self.client.get(
            f"{self.service_url}"
            f"{self.service.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["name"],
            "Cardiology",
        )

    def test_admin_can_create_service(self):

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            self.service_url,
            {
                "name": "Dental",
                "description": "Dental service",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Service.objects.filter(
                name="Dental"
            ).exists()
        )
    def test_admin_can_update_service(self):

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            f"{self.service_url}"
            f"{self.service.id}/",
            {
                "description": "Updated",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.service.refresh_from_db()

        self.assertEqual(
            self.service.description,
            "Updated",
        )
    def test_admin_can_delete_service(self):

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.delete(
            f"{self.service_url}"
            f"{self.service.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Service.objects.filter(
                id=self.service.id
            ).exists()
        )

    def test_doctor_cannot_create_service(self):

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.post(
            self.service_url,
            {
                "name": "Dental",
                "description": "Dental",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_doctor_can_add_service_to_himself(self):

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.post(
            self.doctor_service_url,
            {
                "doctor": self.doctor.id,
                "service": self.service.id,
                "price": "30.00",
                "duration": 30,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            DoctorService.objects.filter(
                doctor=self.doctor,
                service=self.service,
            ).exists()
        )
    def test_doctor_cannot_add_service_to_other_doctor(
        self
    ):

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.post(
            self.doctor_service_url,
            {
                "doctor": self.doctor2.id,
                "service": self.service.id,
                "price": "30.00",
                "duration": 30,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
    def test_admin_can_add_service_to_any_doctor(
        self
    ):

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            self.doctor_service_url,
            {
                "doctor": self.doctor2.id,
                "service": self.service.id,
                "price": "40.00",
                "duration": 45,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_doctor_can_update_his_service(
        self
    ):

        doctor_service = (
            DoctorService.objects.create(
                doctor=self.doctor,
                service=self.service,
                price=30.00,
                duration=30,
            )
        )

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.patch(
            f"{self.doctor_service_url}"
            f"{doctor_service.id}/",
            {
                "price": "35.00",
                "duration": 45,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        doctor_service.refresh_from_db()

        self.assertEqual(
            doctor_service.price,
            Decimal("35.00"),
        )

        self.assertEqual(
            doctor_service.duration,
            45,
        )
    def test_doctor_cannot_update_other_doctors_service(
        self
    ):

        doctor_service = (
            DoctorService.objects.create(
                doctor=self.doctor2,
                service=self.service,
                price=40.00,
                duration=30,
            )
        )

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.patch(
            f"{self.doctor_service_url}"
            f"{doctor_service.id}/",
            {
                "price": "10.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_doctor_can_delete_his_service(
        self
    ):

        doctor_service = (
            DoctorService.objects.create(
                doctor=self.doctor,
                service=self.service,
                price=30.00,
                duration=30,
            )
        )

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.delete(
            f"{self.doctor_service_url}"
            f"{doctor_service.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            DoctorService.objects.filter(
                id=doctor_service.id
            ).exists()
        )
    def test_doctor_cannot_delete_other_doctors_service(
        self
    ):

        doctor_service = (
            DoctorService.objects.create(
                doctor=self.doctor2,
                service=self.service,
                price=40.00,
                duration=30,
            )
        )

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.delete(
            f"{self.doctor_service_url}"
            f"{doctor_service.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_filter_doctors_by_service(
        self
    ):

        DoctorService.objects.create(
            doctor=self.doctor,
            service=self.service,
            price=30.00,
            duration=30,
        )

        DoctorService.objects.create(
            doctor=self.doctor2,
            service=self.service2,
            price=40.00,
            duration=45,
        )

        response = self.client.get(
            f"{self.doctor_service_url}"
            f"?service={self.service.id}"
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
            response.data[0]["doctor"],
            self.doctor.id,
        )
    def test_filter_services_by_doctor(
        self
    ):

        DoctorService.objects.create(
            doctor=self.doctor,
            service=self.service,
            price=30.00,
            duration=30,
        )

        DoctorService.objects.create(
            doctor=self.doctor,
            service=self.service2,
            price=20.00,
            duration=15,
        )

        response = self.client.get(
            f"{self.doctor_service_url}"
            f"?doctor={self.doctor.id}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_same_service_cannot_be_added_twice(
        self
    ):

        DoctorService.objects.create(
            doctor=self.doctor,
            service=self.service,
            price=30.00,
            duration=30,
        )

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.post(
            self.doctor_service_url,
            {
                "doctor": self.doctor.id,
                "service": self.service.id,
                "price": "35.00",
                "duration": 45,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_service_detail_contains_doctors(
        self
    ):

        DoctorService.objects.create(
            doctor=self.doctor,
            service=self.service,
            price=30.00,
            duration=30,
        )

        DoctorService.objects.create(
            doctor=self.doctor2,
            service=self.service,
            price=40.00,
            duration=45,
        )

        response = self.client.get(
            f"{self.service_url}"
            f"{self.service.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data["doctors"]),
            2,
        )

def test_doctor_detail_contains_services(
    self
):

    DoctorService.objects.create(
        doctor=self.doctor,
        service=self.service,
        price=30.00,
        duration=30,
    )

    DoctorService.objects.create(
        doctor=self.doctor,
        service=self.service2,
        price=20.00,
        duration=15,
    )

    self.client.get(
        f"{self.url}{self.doctor.id}/"
    )

    response = self.client.get(
        f"{self.url}{self.doctor.id}/"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK,
    )

    self.assertEqual(
        len(response.data["services"]),
        2,
    )
