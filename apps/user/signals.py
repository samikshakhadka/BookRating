from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.models import CustomUser

@receiver(post_save, sender = CustomUser)
def user_creation(sender, instance, created, **kwargs):
    if created:
        print('A new user is cretated9signal message): ', instance.first_name , instance.email)