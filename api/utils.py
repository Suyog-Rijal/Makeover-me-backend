from django.contrib.auth.tokens import PasswordResetTokenGenerator


def send_verification_email(user):
	print("Sending email to", user.email)
	pass


email_verification_token = PasswordResetTokenGenerator()
