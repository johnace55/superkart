from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomUserProfileForm , CustomUserInfoForm
from accounts.models import CustomUserProfile , CustomUser
from django.contrib import messages
from orders.models import Order , OrderedProduct
import simplejson as json

# Create your views here.

@login_required
def customer_profile(request):
    profile = get_object_or_404(CustomUserProfile , custom_user=request.user)

    if request.method == 'POST':
        profile_form = CustomUserProfileForm(request.POST , instance=profile)
        user_form = CustomUserInfoForm(request.POST , instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request , 'profile updated')
            return redirect('customerprofile')

    else:
        profile_form = CustomUserProfileForm(instance=profile)
        user_form = CustomUserInfoForm(instance=request.user)
    context = {
        'profile_form':profile_form,
        'user_form':user_form,
    }
    return render(request , 'customers/customer_profile.html' , context)


@login_required
def customers_my_orders(request):
    orders = Order.objects.filter(custom_user=request.user , is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders,
    }
    return render(request , 'customers/customers_my_orders.html' , context)


@login_required
def c_order_details(request , order_number):
    try:
        order = Order.objects.get(order_number=order_number , is_ordered=True)
        ordered_product = OrderedProduct.objects.filter(order=order)

        subtotal = 0
        for item in ordered_product:
            subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        context = {
            'order':order,
            'ordered_product':ordered_product,
            'subtotal':subtotal,
            'tax_data':tax_data,
        }
        return render(request , 'customers/c_order_details.html' , context)
    except:
        return redirect('home')




