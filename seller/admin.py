from django.contrib import admin
from seller.models import Seller

# Register your models here.

class SellerAdmin(admin.ModelAdmin):
    list_display = ['custom_user' , 'seller_name' , 'is_approved' , 'created_at']
    list_display_links = ['custom_user' , 'seller_name']

admin.site.register(Seller , SellerAdmin)



