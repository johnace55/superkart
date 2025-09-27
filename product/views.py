from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from product.models import Product , Cart
from accounts.models import CustomUser , CustomUserProfile
from orders.models import Order
from orders.forms import OrderForm


# Create your views here.

@login_required
def cart(request):

    cart_items = Cart.objects.filter(custom_user=request.user).order_by('created_at')

    context = {
        "cart_items":cart_items,
    }

    return render(request , 'product/cart.html' , context)

@login_required
def add_to_cart(request , food_id):
    if request.user.is_authenticated:
            
        product = get_object_or_404(Product , pk=food_id)

        try:
            cart_item = Cart.objects.get(custom_user=request.user , product=product)
            cart_item.quantity += 1
            cart_item.save()
        except Cart.DoesNotExist:
            cart_item = Cart.objects.create(custom_user=request.user , product=product , quantity=1)
        
        return redirect('cart')

            
    else:
        return redirect('login')


@login_required
def decrease_cart(request , food_id):
    
    if request.user.is_authenticated:
        product = Product.objects.get(pk=food_id)
        cart_item = Cart.objects.get(custom_user=request.user , product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')
    else:
        return redirect('login')


@login_required
def remove_cart(request , food_id):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=food_id)
        cart_item = Cart.objects.get(custom_user=request.user , product=product)
        cart_item.delete()
        return redirect('cart')
    else:
        return redirect('login')


@login_required
def checkout(request):

    cart_items = Cart.objects.filter(custom_user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('all_products')
    

    user_profile = CustomUserProfile.objects.get(custom_user=request.user)
    default_values = {
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'phone':request.user.phone_number,
        'email':request.user.email,
        'address':user_profile.address_line_1,
        'country':user_profile.country,
        'state':user_profile.state,
        'city':user_profile.city,
        'pin_code':user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        "form":form,
        'cart_items':cart_items,
    }
    return render(request , 'product/checkout.html' , context)



