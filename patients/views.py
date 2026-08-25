
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import PatientProfile
from .permissions import IsAdminOrSelf
from .serializers import PatientSerializer


class PatientViewSet(
    viewsets.ModelViewSet
):

    queryset = PatientProfile.objects.select_related(
        "user"
    )

    serializer_class = PatientSerializer

    def get_permissions(self):

        if self.action == "list":

            permission_classes = [
                IsAdminUser
            ]

        elif self.action == "retrieve":

            permission_classes = [
                IsAdminOrSelf
            ]

        elif self.action in [
            "update",
            "partial_update",
        ]:

            permission_classes = [
                IsAdminOrSelf
            ]

        elif self.action == "destroy":

            permission_classes = [
                IsAdminUser
            ]

        else:

            permission_classes = [
                IsAdminUser
            ]

        return [
            permission()
            for permission
            in permission_classes
        ]
