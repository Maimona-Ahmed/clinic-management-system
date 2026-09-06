from decimal import Decimal
from datetime import date, time, timedelta

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from doctors.models import (
DoctorProfile,
)
from services.models import DoctorService

from patients.models import PatientProfile

from services.models import Service

from appointments.models import Appointment

from .models import Invoice, Payment

User = get_user_model()

class PaymentAPITestCase(APITestCase):

    def setUp(self):

        self.invoice_url = (
            "/api/payments/invoices/"
        )

        self.payment_url = (
            "/api/payments/payments/"
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
        # Doctor
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
        # Service
        # =================================================

        self.service = (
            Service.objects.create(
                name="General Consultation",
                description="General consultation",
            )
        )

        # =================================================
        # Doctor Service
        # =================================================

        self.doctor_service = (
            DoctorService.objects.create(
                doctor=self.doctor,
                service=self.service,
                price=Decimal("50.00"),
                duration=30,
                is_active=True,
            )
        )

        # =================================================
        # Appointment Date
        # =================================================

        self.appointment_date = (
            date.today()
            + timedelta(days=1)
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
                status=Appointment.Status.CONFIRMED,
                notes="Confirmed appointment",
            )
        )

        # =================================================
        # Invoice
        # =================================================

        self.invoice = (
            Invoice.objects.create(
                appointment=self.appointment,
                amount=Decimal("50.00"),
                status=Invoice.Status.UNPAID,
            )
        )

    # =====================================================
    # Helper
    # =====================================================

    def payment_payload(
        self,
        invoice=None,
        amount="50.00",
        method="CASH",
        transaction_reference="",
    ):

        if invoice is None:
            invoice = self.invoice

        return {
            "invoice": invoice.id,
            "amount": amount,
            "method": method,
            "transaction_reference": (
                transaction_reference
            ),
        }

    # =====================================================
    # INVOICE LIST
    # =====================================================

    def test_patient_can_see_own_invoice(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            self.invoice_url
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
            response.data[0]["id"],
            self.invoice.id,
        )

    # =====================================================
    # PATIENT CANNOT SEE ANOTHER PATIENT INVOICE
    # =====================================================

    def test_patient_cannot_see_another_patient_invoice(
        self
    ):

        other_appointment = (
            Appointment.objects.create(
                patient=self.patient2,
                doctor=self.doctor,
                doctor_service=self.doctor_service,
                appointment_date=(
                    self.appointment_date
                    + timedelta(days=1)
                ),
                appointment_time=time(11, 0),
                status=Appointment.Status.CONFIRMED,
            )
        )

        Invoice.objects.create(
            appointment=other_appointment,
            amount=Decimal("50.00"),
            status=Invoice.Status.UNPAID,
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            self.invoice_url
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
            response.data[0]["id"],
            self.invoice.id,
        )

    # =====================================================
    # DOCTOR CAN SEE OWN INVOICE
    # =====================================================

    def test_doctor_can_see_invoice_for_own_appointment(
        self
    ):

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.get(
            self.invoice_url
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
            response.data[0]["id"],
            self.invoice.id,
        )

    # =====================================================
    # UNAUTHENTICATED INVOICE
    # =====================================================

    def test_unauthenticated_user_cannot_see_invoices(
        self
    ):

        response = self.client.get(
            self.invoice_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    # =====================================================
    # INVOICE DETAIL
    # =====================================================

    def test_patient_can_retrieve_invoice(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            f"{self.invoice_url}"
            f"{self.invoice.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            self.invoice.id,
        )

        self.assertEqual(
            Decimal(
                response.data["amount"]
            ),
            Decimal("50.00"),
        )

        self.assertEqual(
            response.data["status"],
            Invoice.Status.UNPAID,
        )

        self.assertEqual(
            Decimal(
                response.data["remaining_amount"]
            ),
            Decimal("50.00"),
        )

    # =====================================================
    # CREATE PAYMENT
    # =====================================================

    def test_patient_can_create_payment(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.payment_url,
            self.payment_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Payment.objects.count(),
            1,
        )

        payment = (
            Payment.objects.first()
        )

        self.assertEqual(
            payment.invoice,
            self.invoice,
        )

        self.assertEqual(
            payment.amount,
            Decimal("50.00"),
        )

        self.assertEqual(
            payment.method,
            Payment.Method.CASH,
        )

        self.assertEqual(
            payment.status,
            Payment.Status.COMPLETED,
        )

        self.assertIsNotNone(
            payment.paid_at
        )

    # =====================================================
    # PAYMENT MARKS INVOICE AS PAID
    # =====================================================

    def test_full_payment_marks_invoice_as_paid(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.payment_url,
            self.payment_payload(
                amount="50.00"
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.invoice.refresh_from_db()

        self.assertEqual(
            self.invoice.status,
            Invoice.Status.PAID,
        )

    # =====================================================
    # PARTIAL PAYMENT
    # =====================================================

    def test_partial_payment_does_not_mark_invoice_paid(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.payment_url,
            self.payment_payload(
                amount="20.00"
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.invoice.refresh_from_db()

        self.assertEqual(
            self.invoice.status,
            Invoice.Status.UNPAID,
        )

        payment = (
            Payment.objects.first()
        )

        self.assertEqual(
            payment.amount,
            Decimal("20.00"),
        )

    # =====================================================
    # REMAINING AMOUNT
    # =====================================================

    def test_remaining_amount_after_partial_payment(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        self.client.post(
            self.payment_url,
            self.payment_payload(
                amount="20.00"
            ),
            format="json",
        )

        response = self.client.get(
            f"{self.invoice_url}"
            f"{self.invoice.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            Decimal(
                response.data["remaining_amount"]
            ),
            Decimal("30.00"),
        )

    # =====================================================
    # TWO PARTIAL PAYMENTS
    # =====================================================

    def test_two_partial_payments_can_complete_invoice(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response1 = self.client.post(
            self.payment_url,
            self.payment_payload(
                amount="20.00"
            ),
            format="json",
        )

        self.assertEqual(
            response1.status_code,
            status.HTTP_201_CREATED,
        )

        response2 = self.client.post(
            self.payment_url,
            self.payment_payload(
                amount="30.00"
            ),
            format="json",
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_201_CREATED,
        )

        self.invoice.refresh_from_db()

        self.assertEqual(
            self.invoice.status,
            Invoice.Status.PAID,
        )

        self.assertEqual(
            Payment.objects.filter(
                invoice=self.invoice
            ).count(),
            2,
        )

    # =====================================================
    # PAYMENT CANNOT EXCEED INVOICE
    # =====================================================

    def test_payment_cannot_exceed_invoice_amount(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.payment_url,
            self.payment_payload(
                amount="60.00"
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Payment.objects.count(),
            0,
        )

        self.invoice.refresh_from_db()

        self.assertEqual(
            self.invoice.status,
            Invoice.Status.UNPAID,
        )

    # =====================================================
    # ZERO PAYMENT
    # =====================================================

    def test_payment_amount_must_be_greater_than_zero(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.payment_url,
            self.payment_payload(
                amount="0.00"
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Payment.objects.count(),
            0,
        )

    # =====================================================
    # NEGATIVE PAYMENT
    # =====================================================

    def test_negative_payment_is_rejected(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.payment_url,
            self.payment_payload(
                amount="-10.00"
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Payment.objects.count(),
            0,
        )

    # =====================================================
    # PAYMENT ON PAID INVOICE
    # =====================================================

    def test_cannot_pay_already_paid_invoice(
        self
    ):

        self.invoice.status = (
            Invoice.Status.PAID
        )

        self.invoice.save(
            update_fields=["status"]
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.payment_url,
            self.payment_payload(
                amount="50.00"
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Payment.objects.count(),
            0,
        )

    # =====================================================
    # PAYMENT ON CANCELLED INVOICE
    # =====================================================

    def test_cannot_pay_cancelled_invoice(
        self
    ):

        self.invoice.status = (
            Invoice.Status.CANCELLED
        )

        self.invoice.save(
            update_fields=["status"]
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.payment_url,
            self.payment_payload(
                amount="50.00"
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Payment.objects.count(),
            0,
        )

    # =====================================================
    # PAYMENT LIST
    # =====================================================

    def test_patient_can_see_own_payments(
        self
    ):

        Payment.objects.create(
            invoice=self.invoice,
            amount=Decimal("20.00"),
            method=Payment.Method.CASH,
            status=Payment.Status.COMPLETED,
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            self.payment_url
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
            response.data[0]["invoice"],
            self.invoice.id,
        )

    # =====================================================
    # PATIENT CANNOT SEE OTHER PATIENT PAYMENTS
    # =====================================================

    def test_patient_cannot_see_other_patient_payments(
        self
    ):

        other_appointment = (
            Appointment.objects.create(
                patient=self.patient2,
                doctor=self.doctor,
                doctor_service=self.doctor_service,
                appointment_date=(
                    self.appointment_date
                    + timedelta(days=1)
                ),
                appointment_time=time(11, 0),
                status=Appointment.Status.CONFIRMED,
            )
        )

        other_invoice = (
            Invoice.objects.create(
                appointment=other_appointment,
                amount=Decimal("50.00"),
                status=Invoice.Status.UNPAID,
            )
        )

        Payment.objects.create(
            invoice=other_invoice,
            amount=Decimal("50.00"),
            method=Payment.Method.CASH,
            status=Payment.Status.COMPLETED,
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            self.payment_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            0,
        )

    # =====================================================
    # DOCTOR CAN SEE OWN PAYMENTS
    # =====================================================

    def test_doctor_can_see_payments_for_own_appointments(
        self
    ):

        Payment.objects.create(
            invoice=self.invoice,
            amount=Decimal("50.00"),
            method=Payment.Method.CARD,
            status=Payment.Status.COMPLETED,
        )

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.get(
            self.payment_url
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
            response.data[0]["invoice"],
            self.invoice.id,
        )

    # =====================================================
    # DOCTOR CANNOT CREATE PAYMENT
    # =====================================================

    def test_doctor_cannot_create_payment(
        self
    ):

        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.post(
            self.payment_url,
            self.payment_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            Payment.objects.count(),
            0,
        )

    # =====================================================
    # UNAUTHENTICATED PAYMENT
    # =====================================================

    def test_unauthenticated_user_cannot_create_payment(
        self
    ):

        response = self.client.post(
            self.payment_url,
            self.payment_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            Payment.objects.count(),
            0,
        )

    # =====================================================
    # TRANSACTION REFERENCE
    # =====================================================

    def test_payment_transaction_reference_is_saved(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            self.payment_url,
            self.payment_payload(
                amount="50.00",
                method="BANK_TRANSFER",
                transaction_reference=(
                    "TXN-2026-001"
                ),
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        payment = (
            Payment.objects.first()
        )

        self.assertEqual(
            payment.transaction_reference,
            "TXN-2026-001",
        )

        self.assertEqual(
            payment.method,
            Payment.Method.BANK_TRANSFER,
        )

    # =====================================================
    # CANCEL INVOICE
    # =====================================================

    def test_patient_can_cancel_unpaid_invoice(
        self
    ):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            f"{self.invoice_url}"
            f"{self.invoice.id}/cancel/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.invoice.refresh_from_db()

        self.assertEqual(
            self.invoice.status,
            Invoice.Status.CANCELLED,
        )

    # =====================================================
    # CANNOT CANCEL PAID INVOICE
    # =====================================================

    def test_paid_invoice_cannot_be_cancelled(
        self
    ):

        self.invoice.status = (
            Invoice.Status.PAID
        )

        self.invoice.save(
            update_fields=["status"]
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            f"{self.invoice_url}"
            f"{self.invoice.id}/cancel/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.invoice.refresh_from_db()

        self.assertEqual(
            self.invoice.status,
            Invoice.Status.PAID,
        )

    # =====================================================
    # ALREADY CANCELLED
    # =====================================================

    def test_already_cancelled_invoice_cannot_be_cancelled_again(
        self
    ):

        self.invoice.status = (
            Invoice.Status.CANCELLED
        )

        self.invoice.save(
            update_fields=["status"]
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            f"{self.invoice_url}"
            f"{self.invoice.id}/cancel/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.invoice.refresh_from_db()

        self.assertEqual(
            self.invoice.status,
            Invoice.Status.CANCELLED,
        )
