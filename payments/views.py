from rest_framework import (
    status,
    viewsets,
)

from rest_framework.decorators import action

from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework.response import Response

from .models import Invoice, Payment

from .permissions import (
    InvoicePermission,
    PaymentPermission,
)

from .serializers import (
    InvoiceSerializer,
    PaymentSerializer,
)

from .services import (
    cancel_invoice,
    create_payment,
)
from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework.response import Response

from .models import Payment

from .permissions import PaymentPermission

from .serializers import PaymentSerializer

from .services import create_payment




class InvoiceViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = InvoiceSerializer

    permission_classes = [
        IsAuthenticated,
        InvoicePermission,
    ]



    def get_queryset(self):

        user = self.request.user

        queryset = (
            Invoice.objects
            .select_related(
                "appointment",
                "appointment__patient",
                "appointment__doctor",
                "appointment__doctor_service",
                "appointment__doctor_service__service",
            )
            .prefetch_related(
                "payments",
            )
        )



        if hasattr(
            user,
            "patient_profile",
        ):

            return queryset.filter(
                appointment__patient=(
                    user.patient_profile
                )
            )


        if hasattr(
            user,
            "doctor_profile",
        ):

            return queryset.filter(
                appointment__doctor=(
                    user.doctor_profile
                )
            )

        return queryset.none()



    @action(
        detail=True,
        methods=["post"],
    )
    def cancel(
        self,
        request,
        pk=None,
    ):

        invoice = self.get_object()

        invoice = cancel_invoice(
            invoice=invoice
        )

        serializer = self.get_serializer(
            invoice
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )



class PaymentViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = PaymentSerializer

    permission_classes = [
        IsAuthenticated,
        PaymentPermission,
    ]


    def get_queryset(self):

        user = self.request.user

        queryset = (
            Payment.objects
            .select_related(
                "invoice",
                "invoice__appointment",
                "invoice__appointment__patient",
                "invoice__appointment__doctor",
            )
        )


        if hasattr(
            user,
            "patient_profile",
        ):

            return queryset.filter(
                invoice__appointment__patient=(
                    user.patient_profile
                )
            )


        if hasattr(
            user,
            "doctor_profile",
        ):

            return queryset.filter(
                invoice__appointment__doctor=(
                    user.doctor_profile
                )
            )

        return queryset.none()


    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        invoice = serializer.validated_data[
            "invoice"
        ]

        amount = serializer.validated_data[
            "amount"
        ]

        method = serializer.validated_data[
            "method"
        ]

        transaction_reference = (
            serializer.validated_data.get(
                "transaction_reference",
                "",
            )
        )

        payment = create_payment(
            invoice=invoice,
            amount=amount,
            method=method,
            transaction_reference=(
                transaction_reference
            ),
        )

        output_serializer = (
            self.get_serializer(
                payment
            )
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

from rest_framework import (
    status,
    viewsets,
)




class PaymentViewSet(
    viewsets.ModelViewSet
):

    serializer_class = PaymentSerializer

    permission_classes = [
        IsAuthenticated,
        PaymentPermission,
    ]


    def get_queryset(self):

        user = self.request.user

        queryset = (
            Payment.objects
            .select_related(
                "invoice",
                "invoice__appointment",
                "invoice__appointment__patient",
                "invoice__appointment__doctor",
            )
        )

        if hasattr(
            user,
            "patient_profile",
        ):

            return queryset.filter(
                invoice__appointment__patient=(
                    user.patient_profile
                )
            )

        if hasattr(
            user,
            "doctor_profile",
        ):

            return queryset.filter(
                invoice__appointment__doctor=(
                    user.doctor_profile
                )
            )

        return queryset.none()


    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        invoice = serializer.validated_data[
            "invoice"
        ]

        amount = serializer.validated_data[
            "amount"
        ]

        method = serializer.validated_data[
            "method"
        ]

        transaction_reference = (
            serializer.validated_data.get(
                "transaction_reference",
                "",
            )
        )

        payment = create_payment(
            invoice=invoice,
            amount=amount,
            method=method,
            transaction_reference=(
                transaction_reference
            ),
        )

        output_serializer = (
            self.get_serializer(
                payment
            )
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )
