from django.db import models
from accounts.models import CustomUser
from product.models import Product
from seller.models import Seller
import simplejson as json 
import ast

# Create your models here.


request_object = ''

class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PayPal', 'PayPal'),
        ('RazorPay', 'RazorPay'), # Only for Indian Students.
    )
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    sellers = models.ManyToManyField(Seller , blank=True)
    order_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True, null=True , help_text = "Data format: {'tax_type':{'tax_percentage':'tax_amount'}}")
    total_data = models.JSONField(blank=True , null=True)
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def order_placed_to(self):
        return ", ".join([str(i) for i in self.sellers.all()])
    
    def get_total_by_seller(self):
        seller = Seller.objects.get(custom_user=request_object.user)
        subtotal = 0
        tax = 0
        tax_dict = {}
        if self.total_data:
            total_data = json.loads(self.total_data)
            data = total_data.get(str(seller.id))
            
            
            for key , value in data.items():
                subtotal += float(key)
                value_dict = ast.literal_eval(value)
                tax_dict.update(value_dict)

            # {'FBR': {'9.00': '119.88'}, 'WHT': {'7.00': '93.24'}}
                
                for tax_type, tax_info in value_dict.items():
                    #print(tax_info)
                    for percentage , amount in tax_info.items():
                        tax += float(amount)

        grand_total = float(subtotal) + float(tax)
        context = {
            'subtotal':subtotal,
            'tax':tax,
            'tax_dict':tax_dict,
            'grand_total':grand_total,
        }
        return context
    

    def __str__(self):
        return self.order_number


class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_title




