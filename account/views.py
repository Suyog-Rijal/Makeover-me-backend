from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from account.serializers import SignupSerializer, LoginSerializer
from django.conf import settings
from api.tasks import send_email_confirmation_mail
from api.utils import email_verification_token

User = get_user_model()


class SignupView(APIView):
	permission_classes = [AllowAny]

	@extend_schema(tags=['Authentication'], request=SignupSerializer, auth=[])
	def post(self, request):
		serializer = SignupSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()

		if not user.is_verified:
			token = email_verification_token.make_token(user)
			uid = user.pk
			verification_link = f"{settings.FRONTEND_URL}/verify-email/?uid={uid}&token={token}"
			send_email_confirmation_mail.delay(user.email, verification_link)
		return Response({
			'message': 'User created successfully. Please check your email for verification link.' if not user.is_active else 'User created successfully.',
			'data': {
				'id': user.id,
				'email': user.email,
				'full_name': user.full_name,
				'avatar': user.avatar.url if hasattr(user, 'avatar') and user.avatar else None,
			}
		}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
	permission_classes = [AllowAny]
	throttle_scope = 'login_attempts'

	@extend_schema(tags=['Authentication'], request=LoginSerializer, auth=[])
	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']

		refresh = RefreshToken.for_user(user)
		access = refresh.access_token

		return Response({
			'access_token': str(access),
			'refresh_token': str(refresh),
			'data': {
				'id': user.id,
				'email': user.email,
				'full_name': user.full_name,
				'avatar': user.avatar.url if hasattr(user, 'avatar') and user.avatar else None,
			}
		}, status=status.HTTP_200_OK)


class RefreshView(APIView):
	permission_classes = [AllowAny]

	@extend_schema(tags=['Authentication'], request=TokenRefreshSerializer, auth=[])
	def post(self, request):
		serializer = TokenRefreshSerializer(data=request.data)
		try:
			serializer.is_valid(raise_exception=True)
		except TokenError as e:
			return Response({
				"detail": "Invalid or expired token."
			}, status=status.HTTP_401_UNAUTHORIZED)

		return Response(serializer.validated_data, status=status.HTTP_200_OK)


class VerifyEmailView(APIView):
	permission_classes = [AllowAny]

	@extend_schema(tags=['Authentication'], auth=[])
	def get(self, request):
		uid = request.query_params.get('uid')
		token = request.query_params.get('token')

		if not uid or not token:
			return Response({
				"detail": "Invalid verification link."
			}, status=status.HTTP_400_BAD_REQUEST)

		try:
			user = User.objects.get(pk=uid)
		except User.DoesNotExist:
			return Response({
				"detail": "User not found."
			}, status=status.HTTP_404_NOT_FOUND)

		if email_verification_token.check_token(user, token):
			user.is_verified = True
			user.save()
			return Response({
				"detail": "Email verified successfully."
			}, status=status.HTTP_200_OK)
		else:
			return Response({
				"detail": "Invalid verification token."
			}, status=status.HTTP_400_BAD_REQUEST)

