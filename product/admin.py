from django.contrib import admin
from product.models import Category , Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_title',)}
    list_display = ['product_title' , 'category' , 'seller' , 'price' , 'is_available' , 'updated_at']
    search_fields = ['product_title' , 'category__category_name' , 'seller__seller_name' , 'price']
    list_filter = ['is_available']



admin.site.register(Product , ProductAdmin)

admin.site.register(Category)



