from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from patients.models import PatientProfile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    password_confirm = serializers.CharField(write_only = True)
    class Meta:
        model =User
        fields = ["email","first_name","last_name","password","password_confirm"]

    def validate_email(self,value):
        value = value.strip().lower()
        if User.objects.filter(
            email = value
        ).exists():
            raise serializers.ValidationError(" A user with this email already exists")
        return value
    def validate_password(self,value):
        validate_password(value)
        return value
    def validate(self, attrs):
        if(attrs["password"] != attrs["password_confirm"]):
            raise serializers.ValidationError({"password_confirm":"Passwords do not match"})
        return attrs
    
    @transaction.atomic
    def create(self,validated_data):

        validated_data.pop("password_confirm")       
        password = validated_data.pop("password")

        user = User(
            **validated_data,
            role = User.Role.PATIENT
        )
        user.set_password(password)
        user.save()
        PatientProfile.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        email = attrs["email"].strip().lower()
        password = attrs["password"]

        user = authenticate(
            request=self.context.get("request"),
            username = email,
            password = password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive")
        refresh = RefreshToken.for_user(user)
        attrs["refresh"]=str(refresh)
        attrs["access"]=str(refresh.access_token)
        return attrs

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email","first_name","last_name","phone","role"]

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        try:
            refresh = RefreshToken(attrs["refresh"])
            refresh.blacklist()
        except Exception:
            raise serializers.ValidationError("Invalid refresh token")
        return attrs
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only = True)
    new_password = serializers.CharField(write_only = True)
    new_password_confirm = serializers.CharField(write_only = True)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password":"Old password is incorrect"})
        if (attrs["new_password"]!=attrs["new_password_confirm"]):
            raise serializers.ValidationError({"new_password_confirm":"Password do not match"})
        validate_password(attrs["new_password"],user)
        return attrs
    
    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
    
class ForgotPasswordSerializer(
    serializers.Serializer
):

    email = serializers.EmailField()

    def validate_email(self, value):

        return value.strip().lower()


class ResetPasswordSerializer(
    serializers.Serializer
):

    uid = serializers.CharField()

    token = serializers.CharField()

    new_password = serializers.CharField(
        write_only=True
    )

    new_password_confirm = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        try:

            user_id = force_str(
                urlsafe_base64_decode(
                    attrs["uid"]
                )
            )

            user = User.objects.get(
                pk=user_id
            )

        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist
        ):

            raise serializers.ValidationError({
                "uid":
                    "Invalid reset link."
            })

        generator = (
            PasswordResetTokenGenerator()
        )

        if not generator.check_token(
            user,
            attrs["token"]
        ):

            raise serializers.ValidationError({
                "token":
                    "Invalid or expired reset token."
            })

        if (
            attrs["new_password"]
            != attrs["new_password_confirm"]
        ):

            raise serializers.ValidationError({
                "new_password_confirm":
                    "Passwords do not match."
            })

        validate_password(
            attrs["new_password"],
            user
        )

        attrs["user"] = user

        return attrs

    def save(self):

        user = self.validated_data[
            "user"
        ]

        user.set_password(
            self.validated_data[
                "new_password"
            ]
        )

        user.save()

        return user

        
    