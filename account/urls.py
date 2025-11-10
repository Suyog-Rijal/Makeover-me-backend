from django.urls import path
from account.views import SignupView, LoginView, RefreshView, VerifyEmailView, MeView, ForgotPasswordView

urlpatterns = [
	path('signup/', SignupView.as_view(), name='signup'),
	path('login/', LoginView.as_view(), name='login'),
	path('refresh/', RefreshView.as_view(), name='token_refresh'),
	path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
	path('me/', MeView.as_view(), name='me'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password')
]