from django.shortcuts import render , get_object_or_404 , redirect
from seller.forms import SellerForm
from seller.models import Seller
from accounts.forms import CustomUserProfileForm
from accounts.models import CustomUserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required , user_passes_test
from accounts.views import check_role_seller
from product.models import Category , Product
from product.forms import ProductForm
from django.template.defaultfilters import slugify
from django.utils import timezone
from seller.decorators import approved_seller_required
from orders.models import Order , OrderedProduct



# Create your views here.

def get_seller(request):
    seller = Seller.objects.get(custom_user=request.user)
    return seller



@login_required
@user_passes_test(check_role_seller)
def seller_profile(request):


    profile = get_object_or_404(CustomUserProfile , custom_user=request.user)
    seller = get_object_or_404(Seller , custom_user=request.user)

    if request.method == 'POST':
        profile_form = CustomUserProfileForm(request.POST , instance=profile)
        seller_form = SellerForm(request.POST , request.FILES , instance=seller)

        if profile_form.is_valid() and seller_form.is_valid():
            profile_form.save()
            seller_form.save()
            messages.success(request , 'settings updated')
            return redirect('seller_profile')


    else:
        profile_form = CustomUserProfileForm(instance=profile)
        seller_form = SellerForm(instance=seller)
    context = {
        'profile_form':profile_form,
        'seller_form':seller_form,
    }
    return render(request , 'seller/seller_prolfile.html' , context)


@login_required
@user_passes_test(check_role_seller)
def product_builder(request):

    seller = get_seller(request)
    products = Product.objects.filter(seller=seller).order_by('created_at')
    
    context = {
        'products':products,
    }

    return render(request , 'seller/product_builder.html' , context)


@login_required
@user_passes_test(check_role_seller)
@approved_seller_required
def add_product(request):

    if request.method == 'POST':
        form = ProductForm(request.POST , request.FILES)

        if form.is_valid():
            producttitle = form.cleaned_data['product_title']
            product = form.save(commit=False)
            product.seller = get_seller(request)
            product.save()
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            product.slug = f"{slugify(producttitle)}-{product.pk}-{timestamp}"
            product.save()
            messages.success(request , 'product added successfully')
            return redirect('product_builder')

    else:

        form = ProductForm()
    context = {
        'form':form,
    }
    return render(request , 'seller/add_product.html' , context)


@login_required
@user_passes_test(check_role_seller)
@approved_seller_required
def edit_product(request , pk):

    product_obj = get_object_or_404(Product , pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST , request.FILES , instance=product_obj)

        if form.is_valid():
            producttitle = form.cleaned_data['product_title']
            product = form.save(commit=False)
            product.seller = get_seller(request)
            product.save()
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            product.slug = f"{slugify(producttitle)}-{product.pk}-{timestamp}"
            product.save()
            messages.success(request , 'product updated successfully')
            return redirect('product_builder')

    else:

        form = ProductForm(instance=product_obj)
    context = {
        'form':form,
        'product': product_obj, 
    }
    return render(request , 'seller/edit_product.html' , context)

    
@login_required
@user_passes_test(check_role_seller)
@approved_seller_required
def delete_product(request , pk):
    
    product_obj = get_object_or_404(Product , pk=pk)

    product_obj.delete()
    messages.success(request , 'product deleted successfully')
    return redirect("product_builder")


@login_required
@user_passes_test(check_role_seller)
@approved_seller_required
def s_order_details(request , order_number):
    try:
        seller = Seller.objects.get(custom_user=request.user)
        order = Order.objects.get(order_number=order_number , is_ordered=True)
        ordered_product = OrderedProduct.objects.filter(order=order , product__seller=seller)
        context = {
            'order':order,
            'ordered_product':ordered_product,
            'subtotal':order.get_total_by_seller()['subtotal'],
            'tax_dict':order.get_total_by_seller()['tax_dict'],
            'grand_total':order.get_total_by_seller()['grand_total'],
        }
        return render(request , 'seller/s_order_details.html' , context)
    except:
        return redirect('sellerdashboard')

@login_required
@user_passes_test(check_role_seller)
@approved_seller_required
def seller_my_orders(request):
    seller = Seller.objects.get(custom_user=request.user)
    orders = Order.objects.filter(sellers=seller , is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders,
    }
    return render(request , 'seller/seller_my_orders.html' , context)


