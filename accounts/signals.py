from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=EmailAddress)
def sync_email_verified(sender, instance, **kwargs):
    """
    When an EmailAddress is saved, sync its 'verified' status
    to the related user's Profile.
    """
    user = instance.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return

    if instance.primary:
        profile.email_verified = instance.verified
        profile.save(update_fields=["email_verified"])
