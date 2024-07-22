from celery import shared_task
from django.core.mail import send_mail
from apps.user.models import CustomUser

@shared_task
def send_verification_email_task(user_id):
    user = CustomUser.objects.get(id=user_id)
    verification_url = f'http://your-domain.com/verify-email/{user.verification_token}/'
    send_mail(
        'Verify your email',
        f'Please verify your email by clicking on the following link: {verification_url}',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )
