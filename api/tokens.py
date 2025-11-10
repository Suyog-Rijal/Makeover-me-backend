import typing
from django.conf import settings
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired


def generate_token(user_pk: int) -> str:
	signer = signing.TimestampSigner(salt='email-confirmation')
	return signer.sign(str(user_pk))


def verify_token(token: str) -> int:
	signer = signing.TimestampSigner(salt='email-confirmation')
	try:
		unsigned_value = signer.unsign(token, max_age=settings.EMAIL_CONFIRMATION_TOKEN_MAX_AGE)
	except SignatureExpired as e:
		raise signing.SignatureExpired("Verification link expired") from e
	except BadSignature as e:
		raise signing.BadSignature("Invalid verification token") from e

	return int(unsigned_value)