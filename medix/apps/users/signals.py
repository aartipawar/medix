from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from users.models import Profile

@receiver(post_save, sender=User)
def do_something_when_user_updated(sender, instance, created, **kwargs):
    if not created:
        try:
            profile = Profile.objects.get(user=instance)
            if instance.is_active:
                profile.status = 1
            elif not instance.is_active:
                profile.status = 2
            profile.save()
        except Exception as e:
            pass
