from django.db import transaction,models
from django.utils import timezone

from rest_framework.exceptions import ValidationError

from .models import Invoice, Payment



# CREATE INVOICE


@transaction.atomic
def create_invoice(
    *,
    appointment,
):

    # Prevent duplicate invoice


    if Invoice.objects.filter(
        appointment=appointment
    ).exists():

        raise ValidationError({
            "invoice":
                "Invoice already exists "
                "for this appointment."
        })

   
    # Get amount
  

    amount = (
        appointment
        .doctor_service
        .price
    )


    # Validate amount


    if amount <= 0:

        raise ValidationError({
            "amount":
                "Invoice amount must be greater than zero."
        })

  
    # Create invoice


    invoice = Invoice.objects.create(
        appointment=appointment,
        amount=amount,
        status=Invoice.Status.UNPAID,
    )

    return invoice



# CREATE PAYMENT


@transaction.atomic
def create_payment(
    *,
    invoice,
    amount,
    method,
    transaction_reference="",
):


    # Lock invoice


    invoice = (
        Invoice.objects
        .select_for_update()
        .get(
            pk=invoice.pk
        )
    )

    # Check invoice status


    if invoice.status == Invoice.Status.PAID:

        raise ValidationError({
            "invoice":
                "This invoice is already paid."
        })

    if invoice.status == Invoice.Status.CANCELLED:

        raise ValidationError({
            "invoice":
                "Cancelled invoice cannot be paid."
        })


    # Calculate already paid amount
  

    paid_amount = (
        Payment.objects
        .filter(
            invoice=invoice,
            status=Payment.Status.COMPLETED,
        )
        .aggregate(
            total=models.Sum("amount")
        )["total"]
        or 0
    )

   
    # Calculate remaining
   

    remaining_amount = (
        invoice.amount - paid_amount
    )


    # Validate payment amount
  

    if amount <= 0:

        raise ValidationError({
            "amount":
                "Payment amount must be greater than zero."
        })

    if amount > remaining_amount:

        raise ValidationError({
            "amount":
                "Payment amount cannot exceed "
                "the remaining invoice amount."
        })

   
    # Create payment


    payment = Payment.objects.create(
        invoice=invoice,
        amount=amount,
        method=method,
        status=Payment.Status.COMPLETED,
        transaction_reference=(
            transaction_reference
        ),
        paid_at=timezone.now(),
    )

   
    # Check if invoice is fully paid
    

    new_paid_amount = (
        paid_amount + amount
    )

    if new_paid_amount >= invoice.amount:

        invoice.status = Invoice.Status.PAID

        invoice.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

    return payment



# CANCEL INVOICE


@transaction.atomic
def cancel_invoice(
    *,
    invoice,
):

    invoice = (
        Invoice.objects
        .select_for_update()
        .get(
            pk=invoice.pk
        )
    )

    # Already cancelled
    

    if invoice.status == Invoice.Status.CANCELLED:

        raise ValidationError({
            "status":
                "Invoice is already cancelled."
        })

    # Cannot cancel paid invoice
    

    if invoice.status == Invoice.Status.PAID:

        raise ValidationError({
            "status":
                "Paid invoice cannot be cancelled."
        })


    invoice.status = Invoice.Status.CANCELLED

    invoice.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )
    return invoice
