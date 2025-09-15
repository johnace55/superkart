from django.db import models
from accounts.models import CustomUser , CustomUserProfile
from accounts.utils import send_notification_email
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
    
    def save(self , *args , **kwargs):

        if self.pk is not None:
            #update
            orig = Seller.objects.get(pk=self.pk)
            
            if orig != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user':self.custom_user,
                    'is_approved':self.is_approved,
                }
                if self.is_approved == True:
                    mail_subject = 'your restaurant has been approved!'
                
                    send_notification_email(mail_subject , mail_template , context)
                else:
                    mail_subject = 'we are sorry your shop is not approved to sell on this website!'
                    
                    send_notification_email(mail_subject , mail_template , context)
        return super(Seller , self).save(*args , **kwargs)
    





