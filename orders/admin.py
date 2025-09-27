from django.contrib import admin
from orders.models import Payment , Order , OrderedProduct

# Register your models here.

class OrderedProductInLine(admin.TabularInline):
    model = OrderedProduct
    readonly_fields = ['order', 'payment', 'custom_user', 'product', 'quantity', 'price', 'amount']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number' , 'first_name' , 'last_name' , 'phone' , 'email' , 'total' , 'payment_method'  , 'status' , 'is_ordered']
    inlines = [OrderedProductInLine]




admin.site.register(Payment)
admin.site.register(Order , OrderAdmin)
admin.site.register(OrderedProduct)



