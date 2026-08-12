from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, raw=False, **kwargs):
    if raw:
        # Skip during loaddata/fixture loading to avoid UNIQUE constraint conflicts
        return
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
