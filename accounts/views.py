from django.shortcuts import render , redirect
from accounts.forms import CustomerForm
from accounts.models import CustomUser , CustomUserProfile
from django.contrib import messages
from seller.models import Seller
from seller.forms import SellerForm



# Create your views here.

def registercustomer(request):

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():

            # create the user using the form

            #password = form.cleaned_data['password']
            #user = form.save(commit=False)
            #user.set_password(password)
            #user.role = CustomUser.CUSTOMER
            #user.save()

            # create the user using create_user method

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.role = CustomUser.CUSTOMER
            user.save()
            messages.success(request , 'your accounts registerd successfully')

            return redirect('registercustomer')
    else:
        form = CustomerForm()

    context = {
        'form':form,
    }
    return render(request , 'accounts/registercustomer.html' , context)

 

def registerseller(request):

    if request.method == 'POST':

        form = CustomerForm(request.POST)
        s_form = SellerForm(request.POST , request.FILES)

        if form.is_valid() and s_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.role = CustomUser.SELLER
            user.save()

            user_profile = CustomUserProfile.objects.get(custom_user=user)

            seller = s_form.save(commit=False)
            seller.custom_user = user
            seller.seller_profile = user_profile
            seller.save()

            messages.success(request , 'your seller accounts registerd successfully wait for approval')

            return redirect('registerseller')

    else:

        form = CustomerForm()
        s_form = SellerForm()

    context = {
        'form':form,
        's_form':s_form,
    }

    return render(request , 'accounts/registerseller.html' , context)


