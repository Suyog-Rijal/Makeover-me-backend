import re
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(required=True, max_length=255)
	password = serializers.CharField(write_only=True, required=True, min_length=8)

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

	def create(self, validated_data):
		password = validated_data.pop('password')
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		return user


class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField(required=True, max_length=255)
	password = serializers.CharField(write_only=True, required=True)

	def validate(self, attrs):
		email = attrs.get('email')
		password = attrs.get('password')

		user = User.objects.filter(email=email).first()
		if not user:
			raise serializers.ValidationError("Invalid email or password.")
		if not user.check_password(password):
			raise serializers.ValidationError("Invalid email or password.")
		if not user.is_active:
			raise serializers.ValidationError("This account has been disabled. Please contact support.")
		if not user.is_verified:
			raise serializers.ValidationError(
				"Email is not verified. Please check your inbox for the verification email.")
		if user.is_google_user:
			raise serializers.ValidationError(
				"This email is associated with a Google account. Please log in using Google.")

		attrs['user'] = user
		return attrs
