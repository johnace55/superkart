from django.db import models
from accounts.models import CustomUser , CustomUserProfile
# Create your models here.

class Seller(models.Model):
    custom_user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    seller_profile = models.OneToOneField(CustomUserProfile , on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=100)
    seller_license = models.ImageField(upload_to='seller/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.seller_name
    


