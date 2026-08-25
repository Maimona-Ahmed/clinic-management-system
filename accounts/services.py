from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator
)
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import (
    urlsafe_base64_encode
)


User = get_user_model()


def send_password_reset_email(email):

    user = User.objects.filter(
        email=email
    ).first()

    if not user:
        return

    uid = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    token = (
        PasswordResetTokenGenerator()
        .make_token(user)
    )

    reset_url = (
        f"{settings.FRONTEND_URL}"
        f"/reset-password/"
        f"{uid}/{token}/"
    )

    send_mail(
        subject="Reset your password",

        message=(
            "Use the following link "
            "to reset your password:\n\n"
            f"{reset_url}"
        ),

        from_email=(
            settings.DEFAULT_FROM_EMAIL
        ),

        recipient_list=[
            user.email
        ],
    )
