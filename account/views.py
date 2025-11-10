from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signing import SignatureExpired, BadSignature
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import SignupSerializer, LoginSerializer, MeSerializer, ForgotPasswordSerializer
from api.tasks import send_email_confirmation_mail
from api.tokens import generate_token, verify_token

User = get_user_model()


def build_token_response(user, detail_message):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    data = {
        'access_token': str(access),
        'data': {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'avatar': user.avatar.url if hasattr(user, 'avatar') and user.avatar else None,
        },
        'detail': detail_message
    }
    if not settings.PRODUCTION:
        data = {'refresh_token': str(refresh), **data}
    response = Response(data, status=status.HTTP_200_OK)
    if settings.PRODUCTION:
        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE'],
            str(refresh),
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        )
    return response


class SignupView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['Authentication'], request=SignupSerializer, auth=[], summary="Create an account",
                   responses={200: OpenApiResponse(description="Account created successfully")})
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            token = generate_token(user.pk)
            verification_link = f"{settings.FRONTEND_URL}/auth/verify-email?token={token}"
            send_email_confirmation_mail.delay(user.email, verification_link)
            return Response({
                'detail': 'Account created successfully. Please check your email for verification link.',
                'token (STRICTLY for dev env)': f'{verification_link}'
            }, status=status.HTTP_201_CREATED)
        except Exception as ex:
            print(ex)


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = 'login_attempts'

    @extend_schema(tags=['Authentication'], request=LoginSerializer, auth=[], summary="Login a user")
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return build_token_response(user, 'Account has been verified successfully. You can continue your journey')


@method_decorator(csrf_protect, name='dispatch')
class RefreshView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['Authentication'], auth=[], summary="Refresh access token using refresh token")
    def post(self, request):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        if not refresh_token:
            return Response({"detail": "You are not authorized to make this request."},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False):
                if settings.SIMPLE_JWT.get('BLACKLIST_AFTER_ROTATION', False):
                    try:
                        refresh.blacklist()
                    except AttributeError:
                        pass
                user_id = refresh.payload.get('user_id')
                if not user_id:
                    return Response({"detail": "Invalid token payload."}, status=status.HTTP_401_UNAUTHORIZED)
                user = User.objects.filter(id=user_id).first()
                if not user:
                    return Response({"detail": "User not found."}, status=status.HTTP_401_UNAUTHORIZED)
                return build_token_response(user, 'Access token refreshed successfully')
            else:
                access_token = refresh.access_token
                return Response({'access_token': str(access_token)}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_401_UNAUTHORIZED)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['Authentication'], auth=[], summary="Verify email address",
                   parameters=[OpenApiParameter(name='token', type=str, location='query',
                                                description='Email verification token')])
    def get(self, request):
        token = request.query_params.get("token", "")
        try:
            user_pk = verify_token(token)
        except SignatureExpired:
            return Response({"detail": "Link has expired."}, status=status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(pk=user_pk).first()
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        if user.is_verified:
            return Response({"detail": "Account is already verified."}, status=status.HTTP_200_OK)
        user.is_verified = True
        user.save()
        return build_token_response(user, 'Account has been verified successfully. You can continue your journey')


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Authentication'], summary="Get current user details")
    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['Authentication'], auth=[], summary="==============================   In Progress   ==============================", request=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            pass
        except Exception as ex:
            print(ex)
        return Response({
            'detail': 'If an account with this email exists, a password reset link has been sent.'
        }, status=status.HTTP_200_OK)
