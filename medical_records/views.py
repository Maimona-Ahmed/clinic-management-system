from rest_framework import (
    status,
    viewsets,
)

from rest_framework.decorators import (
    action,
)

from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework.response import (
    Response
)

from appointments.models import (
    Appointment,
)

from .models import (
    Consultation,
    Prescription,
    PrescriptionItem,
)

from .permissions import (
    ConsultationPermission,
    PrescriptionItemPermission,
)

from .serializers import (
    ConsultationDetailSerializer,
    DiagnosisSerializer,
    MedicalNoteSerializer,
    PrescriptionSerializer,
    PrescriptionItemSerializer,
    MedicalTestSerializer,
)

from .services import (
    ConsultationService,
)



class ConsultationViewSet(
    viewsets.ReadOnlyModelViewSet
):

    permission_classes = [
        IsAuthenticated,
        ConsultationPermission,
    ]


    def get_queryset(self):

        user = self.request.user

        queryset = (
            Consultation.objects

            .select_related(
                "appointment",
                "appointment__patient",
                "appointment__doctor",
                "appointment__doctor_service",
                "appointment__doctor_service__service",
                "medical_record",
            )

            .prefetch_related(
                "diagnoses",
                "medical_notes",
                "medical_tests",
                "prescription__items",
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

        if hasattr(
            user,
            "patient_profile",
        ):

            return queryset.filter(
                appointment__patient=(
                    user.patient_profile
                )
            )

        return queryset.none()


    def get_serializer_class(self):

        return ConsultationDetailSerializer


    @action(
        detail=False,
        methods=["post"],
        url_path="start",
    )
    def start(
        self,
        request,
    ):


        if not hasattr(
            request.user,
            "doctor_profile",
        ):

            return Response(
                {
                    "detail":
                        "Only doctors can start "
                        "consultations."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        appointment_id = (
            request.data.get(
                "appointment"
            )
        )

        if not appointment_id:

            return Response(
                {
                    "appointment":
                        "Appointment ID is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            appointment = (
                Appointment.objects

                .select_related(
                    "patient",
                    "doctor",
                )

                .get(
                    pk=appointment_id,
                )
            )

        except Appointment.DoesNotExist:

            return Response(
                {
                    "detail":
                        "Appointment not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )


        consultation = (
            ConsultationService
            .start_consultation(
                appointment=appointment,
                doctor=(
                    request.user.doctor_profile
                ),
            )
        )

        serializer = self.get_serializer(
            consultation
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="complete",
    )
    def complete(
        self,
        request,
        pk=None,
    ):


        if not hasattr(
            request.user,
            "doctor_profile",
        ):

            return Response(
                {
                    "detail":
                        "Only doctors can complete "
                        "consultations."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        consultation = self.get_object()

        consultation = (
            ConsultationService
            .complete_consultation(
                consultation=consultation,
                doctor=(
                    request.user.doctor_profile
                ),
            )
        )

        serializer = self.get_serializer(
            consultation
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["get", "post"],
        url_path="diagnoses",
    )
    def diagnoses(
        self,
        request,
        pk=None,
    ):

        consultation = self.get_object()

        if request.method == "GET":

            diagnoses = (
                consultation
                .diagnoses
                .all()
            )

            serializer = DiagnosisSerializer(
                diagnoses,
                many=True,
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        serializer = DiagnosisSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        diagnosis = serializer.save(
            consultation=consultation,
        )

        return Response(
            DiagnosisSerializer(
                diagnosis
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["get", "post"],
        url_path="notes",
    )
    def notes(
        self,
        request,
        pk=None,
    ):

        consultation = self.get_object()

        if request.method == "GET":

            notes = (
                consultation
                .medical_notes
                .all()
            )

            serializer = MedicalNoteSerializer(
                notes,
                many=True,
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        serializer = MedicalNoteSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        note = serializer.save(
            consultation=consultation,
        )

        return Response(
            MedicalNoteSerializer(
                note
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["get", "post"],
        url_path="prescription",
    )
    def prescription(
        self,
        request,
        pk=None,
    ):

        consultation = self.get_object()

        if request.method == "GET":

            try:

                prescription = (
                    consultation
                    .prescription
                )

            except Prescription.DoesNotExist:

                return Response(
                    {
                        "detail":
                            "Prescription does not exist."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = (
                PrescriptionSerializer(
                    prescription
                )
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        serializer = PrescriptionSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        prescription = (
            ConsultationService
            .create_prescription(
                consultation=consultation,
                notes=serializer
                .validated_data
                .get(
                    "notes",
                    "",
                ),
            )
        )

        return Response(
            PrescriptionSerializer(
                prescription
            ).data,
            status=status.HTTP_201_CREATED,
        )


    @action(
        detail=True,
        methods=["get", "post"],
        url_path="tests",
    )
    def tests(
        self,
        request,
        pk=None,
    ):

        consultation = self.get_object()

        if request.method == "GET":

            tests = (
                consultation
                .medical_tests
                .all()
            )

            serializer = MedicalTestSerializer(
                tests,
                many=True,
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        serializer = MedicalTestSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        medical_test = serializer.save(
            consultation=consultation,
        )

        return Response(
            MedicalTestSerializer(
                medical_test
            ).data,
            status=status.HTTP_201_CREATED,
        )


class PrescriptionItemViewSet(
    viewsets.ModelViewSet
):

    serializer_class = (
        PrescriptionItemSerializer
    )

    permission_classes = [
        IsAuthenticated,
        PrescriptionItemPermission,
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = (
            PrescriptionItem.objects

            .select_related(
                "prescription",
                "prescription__consultation",
                "prescription__consultation__appointment",
                "prescription__consultation__appointment__doctor",
                "prescription__consultation__appointment__patient",
            )
        )

        if hasattr(
            user,
            "doctor_profile",
        ):

            return queryset.filter(
                prescription__consultation__appointment__doctor=(
                    user.doctor_profile
                )
            )

        if hasattr(
            user,
            "patient_profile",
        ):

            return queryset.filter(
                prescription__consultation__appointment__patient=(
                    user.patient_profile
                )
            )

        return queryset.none()

    def perform_create(
        self,
        serializer,
    ):

        prescription_id = (
            self.request.data.get(
                "prescription"
            )
        )

        try:

            prescription = (
                Prescription.objects
                .get(
                    pk=prescription_id
                )
            )

        except Prescription.DoesNotExist:

            from rest_framework.exceptions import (
                ValidationError,
            )

            raise ValidationError({
                "prescription":
                    "Prescription not found."
            })

        if (
            self.request.user.doctor_profile
            != prescription
            .consultation
            .appointment
            .doctor
        ):

            from rest_framework.exceptions import (
                PermissionDenied,
            )

            raise PermissionDenied(
                "You cannot modify this prescription."
            )

        serializer.save(
            prescription=prescription
        )

