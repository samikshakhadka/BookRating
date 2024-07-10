from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.user.models import CustomUser

User = get_user_model()

def send_verification_email(user):
    verification_url = f"{settings.SITE_URL}{reverse('verify-email', args=[user.verification_token])}"
    subject = 'Verify your email'
    message = f'Hi {user.email}, please verify your email by clicking the link: {verification_url}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
