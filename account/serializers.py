import re

from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.tasks import send_email_confirmation_mail
from api.tokens import generate_email_confirmation_token

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    contact = serializers.CharField(required=True, max_length=10)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'contact', 'password')

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if user:
            message = (
                "A Google account is associated with this email. Please continue with Google to access your account."
                if user.is_google_user else
                "An account with this email already exists. Please log in or use a different email to sign up."
            )
            raise serializers.ValidationError(message)
        return value

    def validate_password(self, value):
        rules = [
            (r'[A-Z]', "uppercase letter"),
            (r'[a-z]', "lowercase letter"),
            (r'\d', "number"),
            (r'[^\w\s]', "special character"),
        ]
        for pattern, label in rules:
            if not re.search(pattern, value):
                raise serializers.ValidationError(f"Password must include at least one {label}.")
        return value

    def validate_contact(self, value):
        if not re.fullmatch(r'9[6-9]\d{8}', value):
            raise serializers.ValidationError("Invalid mobile number.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(write_only=True, required=True)
    secure = serializers.BooleanField(required=False, default=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account has been disabled. Please contact support.")
        if user.is_google_user:
            raise serializers.ValidationError(
                "This email is associated with a Google account. Please log in using Google.")
        if not user.is_verified:
            token = generate_email_confirmation_token(user.pk)
            verification_link = f"{settings.FRONTEND_URL}/auth/verify-email?token={token}"
            send_email_confirmation_mail.delay(user.email, verification_link)
            raise serializers.ValidationError(
                "Email is not verified. Please check your inbox and verify the email clicking the verification link.")

        attrs['user'] = user
        return attrs


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'contact', 'avatar')
