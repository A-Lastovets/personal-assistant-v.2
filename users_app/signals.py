from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            avatar='https://sudoteam.s3.eu-north-1.amazonaws.com/default_avatar.png',
            phone='',
            address='',
            gender='other'
        )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
