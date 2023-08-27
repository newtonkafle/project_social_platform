"""
this file contains the necessary singals for the database
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """create a profile of user using django signal post_save """
    try:
        profile = Profile.objects.get(user=instance)
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
    else:
        profile.save()
