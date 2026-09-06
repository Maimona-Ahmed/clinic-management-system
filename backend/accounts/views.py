from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    MeSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

from .services import (
    send_password_reset_email
)


class RegisterView(
    generics.CreateAPIView
):

    serializer_class = (
        RegisterSerializer
    )


class LoginView(
    generics.GenericAPIView
):

    serializer_class = (
        LoginSerializer
    )

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        return Response(
            {
                "access":
                    serializer.validated_data[
                        "access"
                    ],

                "refresh":
                    serializer.validated_data[
                        "refresh"
                    ],
            },
            status=status.HTTP_200_OK
        )


class MeView(
    generics.RetrieveAPIView
):

    serializer_class = MeSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self):

        return self.request.user


class LogoutView(
    generics.GenericAPIView
):

    serializer_class = (
        LogoutSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        return Response(
            {
                "detail":
                    "Successfully logged out."
            },
            status=status.HTTP_200_OK
        )


class ChangePasswordView(
    generics.GenericAPIView
):

    serializer_class = (
        ChangePasswordSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "detail":
                    "Password changed successfully."
            },
            status=status.HTTP_200_OK
        )


class ForgotPasswordView(
    generics.GenericAPIView
):

    serializer_class = (
        ForgotPasswordSerializer
    )

    permission_classes = []

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        send_password_reset_email(
            serializer.validated_data[
                "email"
            ]
        )

        return Response(
            {
                "detail":
                    "If an account exists, "
                    "a password reset link has "
                    "been sent."
            },
            status=status.HTTP_200_OK
        )


class ResetPasswordView(
    generics.GenericAPIView
):

    serializer_class = (
        ResetPasswordSerializer
    )

    permission_classes = []

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "detail":
                    "Password reset successfully."
            },
            status=status.HTTP_200_OK
        )
