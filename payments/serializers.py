from rest_framework import serializers

from .models import Invoice, Payment


class PaymentSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Payment

        fields = [
            "id",
            "invoice",
            "amount",
            "method",
            "status",
            "transaction_reference",
            "paid_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "paid_at",
            "created_at",
            "updated_at",
        ]


class InvoiceSerializer(
    serializers.ModelSerializer
):

    payments = PaymentSerializer(
        many=True,
        read_only=True,
    )

    remaining_amount = serializers.SerializerMethodField()

    class Meta:
        model = Invoice

        fields = [
            "id",
            "appointment",
            "amount",
            "status",
            "remaining_amount",
            "payments",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "remaining_amount",
            "payments",
            "created_at",
            "updated_at",
        ]

    def get_remaining_amount(
        self,
        obj,
    ):

        paid_amount = sum(
            payment.amount
            for payment in obj.payments.all()
            if payment.status
            == Payment.Status.COMPLETED
        )

        return max(
            obj.amount - paid_amount,
            0
        )
