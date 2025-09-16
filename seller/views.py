from django.shortcuts import render , get_object_or_404 , redirect
from seller.forms import SellerForm
from seller.models import Seller
from accounts.forms import CustomUserProfileForm
from accounts.models import CustomUserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required , user_passes_test
from accounts.views import check_role_customer


# Create your views here.

@login_required
@user_passes_test(check_role_customer)
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



