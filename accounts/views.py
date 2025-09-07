from django.shortcuts import render , redirect
from accounts.forms import CustomerForm
from accounts.models import CustomUser , CustomUserProfile
from django.contrib import messages
from seller.models import Seller
from seller.forms import SellerForm
from django.contrib import auth
from accounts.utils import detectuser
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.exceptions import PermissionDenied



# Create your views here.



# restrict the seller from accessing the customer page

def check_role_seller(user):
    
    if user.role == 1:
        return True
    else:
        raise PermissionDenied



# restrict the customer from accessing the seller page


def check_role_customer(user):
    
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    


def registercustomer(request):

    if request.user.is_authenticated:
        messages.warning(request , 'you are already logged in!')
        return redirect('myAccount')

    elif request.method == 'POST':
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


    if request.user.is_authenticated:
        messages.warning(request , 'you are already logged in!')
        return redirect('myAccount')

    elif request.method == 'POST':

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


def login(request):

    if request.user.is_authenticated:
        messages.warning(request , 'you are already logged in!')
        return redirect('myAccount')

    elif request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email , password=password)
        if user is not None:

            auth.login(request , user)

            messages.success(request , 'your are now logged in')
            return redirect('myAccount')
        else:
            messages.success(request , 'invalid credentials')
            return redirect('login')
        

    return render(request , 'accounts/login.html')



def logout(request):



    if request.method == 'POST':

        auth.logout(request)

        messages.info(request , 'You are now logged out!')

        return redirect('login')
    






@login_required
def myAccount(request):

    user = request.user
    redirecturl = detectuser(user=user)

    return redirect(redirecturl)



@login_required
@user_passes_test(check_role_customer)
def customerdashboard(request):
    return render(request , 'accounts/customerdashboard.html')


@login_required
@user_passes_test(check_role_seller)
def sellerdashboard(request):
    return render(request , 'accounts/sellerdashboard.html')





