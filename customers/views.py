from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomUserProfileForm , CustomUserInfoForm
from accounts.models import CustomUserProfile , CustomUser
from django.contrib import messages

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



