from django.shortcuts import render , get_object_or_404
from product.models import Product , Category
from seller.models import Seller

# Create your views here.

def home(request):
    products = Product.objects.filter(is_available=True)[:8]
    context = {
        'products':products,
    }
    return render(request , 'tut/home.html' , context)


def product_detail(request , slug):

    product = Product.objects.get(slug=slug)

    context = {
        'product':product,
    }


    return render(request , 'tut/product_detail.html' , context)


def all_products(request , category=None):

    if category:
        category_obj = get_object_or_404(Category , category_name=category)
        products = Product.objects.filter(category=category_obj, is_available=True)

    else:
        products = Product.objects.filter(is_available=True)

    product = products.count()

    categories = Category.objects.all()

    context = {
        'products':products,
        'product':product,
        'categories':categories,
    }
    return render(request , 'tut/all_products.html' , context)


def seller_store(request , store_name):

    seller = Seller.objects.get(seller_name=store_name)

    products = Product.objects.filter(seller=seller , is_available=True)

    context = {
        'seller':seller,
        'products':products,
    }


    return render(request , 'tut/seller_store.html' , context)
   


