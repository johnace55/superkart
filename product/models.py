from django.db import models
from seller.models import Seller
from accounts.models import CustomUser

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200 , unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.category_name
    
    
class Product(models.Model):
    seller = models.ForeignKey(Seller , on_delete=models.CASCADE)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    product_title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200 , unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    image = models.ImageField(upload_to='productimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product_title 


class Cart(models.Model):
    custom_user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.custom_user.username





