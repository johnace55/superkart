from django.shortcuts import render , get_object_or_404 , HttpResponse
from product.models import Product , Category , Cart
from seller.models import Seller
from django.core.paginator import EmptyPage , PageNotAnInteger , Paginator
from django.db.models import Q

# Create your views here.

def home(request):
    products = Product.objects.filter(is_available=True)[:8]
    context = {
        'products':products,
    }
    return render(request , 'tut/home.html' , context)


def product_detail(request , slug):

    product = Product.objects.get(slug=slug)

    in_cart = Cart.objects.filter(product=product , custom_user=request.user).exists()

    context = {
        'product':product,
        'in_cart':in_cart,
    }


    return render(request , 'tut/product_detail.html' , context)


def all_products(request , category=None):

    if category:
        category_obj = get_object_or_404(Category , category_name=category)
        products = Product.objects.filter(category=category_obj, is_available=True).order_by('id')
        paginator = Paginator(products , 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products , 2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)




    categories = Category.objects.all()

    cart_products = []
    if request.user.is_authenticated:
        cart_products = Cart.objects.filter(custom_user=request.user).values_list("product_id", flat=True)
    

    context = {
        'products':paged_products,
        'categories':categories,
        'cart_products':cart_products,
    }
    return render(request , 'tut/all_products.html' , context)






def seller_store(request , store_name):

    seller = Seller.objects.get(seller_name=store_name)

    products = Product.objects.filter(seller=seller , is_available=True).order_by('id')
    paginator = Paginator(products , 2)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)


    
    cart_products = []
    if request.user.is_authenticated:
        cart_products = Cart.objects.filter(custom_user=request.user).values_list("product_id", flat=True)


    context = {
        'seller':seller,
        'products':paged_products,
        'cart_products':cart_products,
    }


    return render(request , 'tut/seller_store.html' , context)
   


def search(request):
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(is_available=True) & Q(description__icontains=keyword) | Q(product_title__icontains=keyword))

    context = {
        'products':products,
    }

    return render(request , 'tut/all_products.html' , context)




