from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email_confirmation_mail(email, verification_link):
    allowed_emails = ['punmanoj2060@gmail.com', 'rijalsuyog75@gmail.com', 'businessmanoj01@gmail.com ']
    if email in allowed_emails:
        subject = 'Verify Your Email Address'
        message = f'Please click the following link to verify your email:\n\n{verification_link}\n\nIf you did not request this, you can ignore this email.'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
    else:
        print(f"Skipped sending email to: {email}")

