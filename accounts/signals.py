from django.db.models.signals import post_save
from accounts.models import CustomUser , CustomUserProfile
from django.dispatch import receiver


@receiver(post_save , sender=CustomUser)
def post_save_create_profile_receiver(sender , instance , created , **kwargs):
    
    if created:
        CustomUserProfile.objects.create(custom_user=instance)
    else:
        try:
            profile = CustomUserProfile.objects.get(custom_user=instance)
            profile.save()
        except:
            CustomUserProfile.objects.create(custom_user=instance)

            






