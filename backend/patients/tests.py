
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from patients.models import PatientProfile


User = get_user_model()


class PatientViewSetTestCase(
    APITestCase
):

    def setUp(self):

        self.url = "/api/patients/"

        self.patient_user = (
            User.objects.create_user(
                email="patient@example.com",
                password="StrongPassword123!",
                first_name="Sara",
                last_name="Ahmed",
                phone="777777777",
                role=User.Role.PATIENT,
            )
        )

        self.patient = (
            PatientProfile.objects.create(
                user=self.patient_user,
                date_of_birth="2000-01-01",
                gender=PatientProfile.Gender.FEMALE,
                blood_type="O+",
                address="Sana'a",
                emergency_contact_name="Ahmed Ahmed",
                emergency_contact_phone="711111111",
            )
        )

        self.other_patient_user = (
            User.objects.create_user(
                email="other@example.com",
                password="StrongPassword123!",
                first_name="Ali",
                last_name="Hassan",
                role=User.Role.PATIENT,
            )
        )

        self.other_patient = (
            PatientProfile.objects.create(
                user=self.other_patient_user
            )
        )

        self.admin = (
            User.objects.create_superuser(
                email="admin@example.com",
                password="StrongPassword123!",
            )
        )

    # --------------------------------
    # LIST
    # --------------------------------

    def test_patient_cannot_list_patients(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_admin_can_list_patients(
        self
    ):

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            2
        )

    # --------------------------------
    # RETRIEVE
    # --------------------------------

    def test_patient_can_view_own_profile(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            f"{self.url}{self.patient.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["email"],
            "patient@example.com"
        )

    def test_patient_cannot_view_other_patient(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            f"{self.url}{self.other_patient.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_admin_can_view_patient(
        self
    ):

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            f"{self.url}{self.patient.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # --------------------------------
    # UPDATE
    # --------------------------------

    def test_patient_can_update_own_profile(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.patch(
            f"{self.url}{self.patient.id}/",
            {
                "address": "New Address",
                "emergency_contact_phone": "722222222",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.patient.refresh_from_db()

        self.assertEqual(
            self.patient.address,
            "New Address"
        )

    def test_patient_cannot_update_other_patient(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.patch(
            f"{self.url}{self.other_patient.id}/",
            {
                "address": "Hacked Address",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_admin_can_update_patient(
        self
    ):

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            f"{self.url}{self.patient.id}/",
            {
                "address": "Admin Updated Address",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # --------------------------------
    # DELETE
    # --------------------------------

    def test_patient_cannot_delete_patient(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.delete(
            f"{self.url}{self.patient.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_admin_can_delete_patient(
        self
    ):

        self.client.force_authenticate(
            user=self.admin
        )

        patient_id = self.patient.id

        response = self.client.delete(
            f"{self.url}{patient_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            PatientProfile.objects.filter(
                id=patient_id
            ).exists()
        )
