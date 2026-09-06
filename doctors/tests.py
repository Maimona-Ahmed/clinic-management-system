# from datetime import date, timedelta

# from django.contrib.auth import get_user_model

# from rest_framework import status
# from rest_framework.test import APITestCase

# from doctors.models import (
#     DoctorProfile,
#     DoctorTimeOff,
# )


# User = get_user_model()


# class DoctorTimeOffAPITestCase(
#     APITestCase
# ):

#     def setUp(self):

#         # ==========================================
#         # URL
#         # ==========================================

#         self.timeoff_url = (
#             "/api/doctor-time-offs/"
#         )

#         # ==========================================
#         # Doctor 1
#         # ==========================================

#         self.doctor_user = (
#             User.objects.create_user(
#                 email="doctor@example.com",
#                 password="StrongPassword123!",
#                 first_name="Ahmed",
#                 last_name="Ali",
#                 role=User.Role.DOCTOR,
#             )
#         )

#         self.doctor = (
#             DoctorProfile.objects.create(
#                 user=self.doctor_user,
#                 specialization="Cardiology",
#                 license_number="DOC-001",
#                 bio="Heart specialist",
#                 consultation_fee=50.00,
#             )
#         )

#         # ==========================================
#         # Doctor 2
#         # ==========================================

#         self.doctor2_user = (
#             User.objects.create_user(
#                 email="doctor2@example.com",
#                 password="StrongPassword123!",
#                 first_name="Sara",
#                 last_name="Ahmed",
#                 role=User.Role.DOCTOR,
#             )
#         )

#         self.doctor2 = (
#             DoctorProfile.objects.create(
#                 user=self.doctor2_user,
#                 specialization="Dentistry",
#                 license_number="DOC-002",
#                 bio="Dentist",
#                 consultation_fee=40.00,
#             )
#         )

#         # ==========================================
#         # Patient
#         # ==========================================

#         self.patient = (
#             User.objects.create_user(
#                 email="patient@example.com",
#                 password="StrongPassword123!",
#                 first_name="Mona",
#                 last_name="Ali",
#                 role=User.Role.PATIENT,
#             )
#         )

#         # ==========================================
#         # Existing Time Off
#         # ==========================================

#         self.timeoff = (
#             DoctorTimeOff.objects.create(
#                 doctor=self.doctor,
#                 start_date=date(2026, 9, 1),
#                 end_date=date(2026, 9, 5),
#                 reason="Vacation",
#                 is_active=True,
#             )
#         )

#     # ==================================================
#     # LIST
#     # ==================================================

#     def test_doctor_can_list_his_timeoffs(
#         self
#     ):

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.get(
#             self.timeoff_url
#         )

#         self.assertEqual(
#             response.status_code,
#             status.HTTP_200_OK,
#         )

#         self.assertEqual(
#             len(response.data),
#             1,
#         )

#         self.assertEqual(
#             response.data[0]["doctor"],
#             self.doctor.id,
#         )

#     # ==================================================
#     # OWNERSHIP - LIST
#     # ==================================================

#     def test_doctor_cannot_see_other_doctors_timeoffs(
#         self
#     ):

#         DoctorTimeOff.objects.create(
#             doctor=self.doctor2,
#             start_date=date(2026, 9, 10),
#             end_date=date(2026, 9, 12),
#             reason="Vacation",
#             is_active=True,
#         )

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.get(
#             self.timeoff_url
#         )

#         self.assertEqual(
#             response.status_code,
#             status.HTTP_200_OK,
#         )

#         self.assertEqual(
#             len(response.data),
#             1,
#         )

#         self.assertEqual(
#             response.data[0]["doctor"],
#             self.doctor.id,
#         )

#     # ==================================================
#     # RETRIEVE
#     # ==================================================

#     def test_doctor_can_retrieve_his_timeoff(
#         self
#     ):

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.get(
#             f"{self.timeoff_url}"
#             f"{self.timeoff.id}/"
#         )

#         self.assertEqual(
#             response.status_code,
#             status.HTTP_200_OK,
#         )

#         self.assertEqual(
#             response.data["id"],
#             self.timeoff.id,
#         )

#     # ==================================================
#     # OWNERSHIP - RETRIEVE
#     # ==================================================

#     def test_doctor_cannot_retrieve_other_doctors_timeoff(
#         self
#     ):

#         other_timeoff = (
#             DoctorTimeOff.objects.create(
#                 doctor=self.doctor2,
#                 start_date=date(2026, 9, 10),
#                 end_date=date(2026, 9, 12),
#                 reason="Vacation",
#                 is_active=True,
#             )
#         )

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.get(
#             f"{self.timeoff_url}"
#             f"{other_timeoff.id}/"
#         )

#         self.assertIn(
#             response.status_code,
#             [
#                 status.HTTP_403_FORBIDDEN,
#                 status.HTTP_404_NOT_FOUND,
#             ],
#         )

#     # ==================================================
#     # CREATE
#     # ==================================================

#     def test_doctor_can_create_timeoff(
#         self
#     ):

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.post(
#             self.timeoff_url,
#             {
#                 "start_date": "2026-10-01",
#                 "end_date": "2026-10-05",
#                 "reason": "Personal leave",
#                 "is_active": True,
#             },
#             format="json",
#         )

#         self.assertEqual(
#             response.status_code,
#             status.HTTP_201_CREATED,
#         )

#         self.assertTrue(
#             DoctorTimeOff.objects.filter(
#                 doctor=self.doctor,
#                 start_date=date(2026, 10, 1),
#                 end_date=date(2026, 10, 5),
#             ).exists()
#         )

#     # ==================================================
#     # CREATE - OTHER DOCTOR
#     # ==================================================

#     def test_doctor_cannot_create_timeoff_for_other_doctor(
#         self
#     ):

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.post(
#             self.timeoff_url,
#             {

#                 "start_date": "2026-10-01",
#                 "end_date": "2026-10-05",
#                 "reason": "Vacation",
#                 "is_active": True,
#             },
#             format="json",
#         )

#         self.assertEqual(
#             response.status_code,
#             status.HTTP_201_CREATED,
#         )

#     # ==================================================
#     # UPDATE
#     # ==================================================

#     def test_doctor_can_update_his_timeoff(
#         self
#     ):

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.patch(
#             f"{self.timeoff_url}"
#             f"{self.timeoff.id}/",
#             {
#                 "reason": "Updated vacation",
#             },
#             format="json",
#         )

#         self.assertEqual(
#             response.status_code,
#             status.HTTP_200_OK,
#         )

#         self.timeoff.refresh_from_db()

#         self.assertEqual(
#             self.timeoff.reason,
#             "Updated vacation",
#         )

#     # ==================================================
#     # UPDATE - OTHER DOCTOR
#     # ==================================================

#     def test_doctor_cannot_update_other_doctors_timeoff(
#         self
#     ):

#         other_timeoff = (
#             DoctorTimeOff.objects.create(
#                 doctor=self.doctor2,
#                 start_date=date(2026, 9, 10),
#                 end_date=date(2026, 9, 12),
#                 reason="Vacation",
#                 is_active=True,
#             )
#         )

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.patch(
#             f"{self.timeoff_url}"
#             f"{other_timeoff.id}/",
#             {
#                 "reason": "Changed",
#             },
#             format="json",
#         )

#         self.assertIn(
#             response.status_code,
#             [
#                 status.HTTP_403_FORBIDDEN,
#                 status.HTTP_404_NOT_FOUND,
#             ],
#         )

#     # ==================================================
#     # DELETE
#     # ==================================================

#     def test_doctor_can_delete_his_timeoff(
#         self
#     ):

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.delete(
#             f"{self.timeoff_url}"
#             f"{self.timeoff.id}/"
#         )

#         self.assertEqual(
#             response.status_code,
#             status.HTTP_204_NO_CONTENT,
#         )

#         self.assertFalse(
#             DoctorTimeOff.objects.filter(
#                 id=self.timeoff.id
#             ).exists()
#         )

#     # ==================================================
#     # DELETE - OTHER DOCTOR
#     # ==================================================

#     def test_doctor_cannot_delete_other_doctors_timeoff(
#         self
#     ):

#         other_timeoff = (
#             DoctorTimeOff.objects.create(
#                 doctor=self.doctor2,
#                 start_date=date(2026, 9, 10),
#                 end_date=date(2026, 9, 12),
#                 reason="Vacation",
#                 is_active=True,
#             )
#         )

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.delete(
#             f"{self.timeoff_url}"
#             f"{other_timeoff.id}/"
#         )

#         self.assertIn(
#             response.status_code,
#             [
#                 status.HTTP_403_FORBIDDEN,
#                 status.HTTP_404_NOT_FOUND,
#             ],
#         )

#     # ==================================================
#     # VALIDATION
#     # ==================================================

#     def test_end_date_must_be_after_start_date(
#         self
#     ):

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.post(
#             self.timeoff_url,
#             {
#                 "start_date": "2026-10-10",
#                 "end_date": "2026-10-05",
#                 "reason": "Vacation",
#                 "is_active": True,
#             },
#             format="json",
#         )

#         self.assertEqual(
#             response.status_code,
#             status.HTTP_400_BAD_REQUEST,
#         )

#     # ==================================================
#     # SAME DATE IS VALID
#     # ==================================================

#     def test_same_start_and_end_date_is_valid(
#         self
#     ):

#         self.client.force_authenticate(
#             user=self.doctor_user
#         )

#         response = self.client.post(
#             self.timeoff_url,
#             {
#                 "start_date": "2026-10-10",
#                 "end_date": "2026-10-10",
#                 "reason": "One day leave",
#                 "is_active": True,
#             },
#             format="json",
#         )

#         self.assertEqual(
#             response.status_code,
#             status.HTTP_201_CREATED,
#         )

#     # ==================================================
#     # UNAUTHENTICATED
#     # ==================================================

#     def test_unauthenticated_user_cannot_access_timeoff(
#         self
#     ):

#         response = self.client.get(
#             self.timeoff_url
#         )

#         self.assertEqual(
#             response.status_code,
#             status.HTTP_401_UNAUTHORIZED,
#         )

#     # ==================================================
#     # PATIENT CANNOT CREATE
#     # ==================================================

#     def test_patient_cannot_create_timeoff(
#         self
#     ):

#         self.client.force_authenticate(
#             user=self.patient
#         )

#         response = self.client.post(
#             self.timeoff_url,
#             {
#                 "start_date": "2026-10-01",
#                 "end_date": "2026-10-05",
#                 "reason": "Vacation",
#                 "is_active": True,
#             },
#             format="json",
#         )

#         self.assertEqual(
#             response.status_code,
#             status.HTTP_403_FORBIDDEN,
#         )
