from django.shortcuts import render , redirect
from accounts.forms import CustomerForm
from accounts.models import CustomUser , CustomUserProfile
from django.contrib import messages
from seller.models import Seller
from seller.forms import SellerForm
from django.contrib import auth
from accounts.utils import detectuser , send_verification_email 
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from orders.models import Order
from datetime import datetime



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

            # send verification email


            mail_subject = 'please activate your account'

            email_template = 'accounts/emails/accounts_verification_email.html'

            send_verification_email(request , user , mail_subject , email_template)

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

            # send verification email

            mail_subject = 'please activate your account'

            email_template = 'accounts/emails/accounts_verification_email.html'

            send_verification_email(request , user , mail_subject , email_template)

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



def activate(request , uidb64 , token):
    # activate the user by setting the is_active status to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except(TypeError , ValueError , OverflowError , CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user , token):
        user.is_active = True
        user.save()
        messages.success(request , 'congrats your account is activated')
        return redirect('myAccount')
    else:
        messages.error(request , 'invalid link')
        return redirect('myAccount')



def forgot_password(request):

    if request.method == 'POST':

        email = request.POST['email']

        if CustomUser.objects.filter(email=email).exists():

            user = CustomUser.objects.get(email__exact=email)

            # send reset password email

            mail_subject = 'reset your password'

            email_template = 'accounts/emails/reset_password_email.html'

            send_verification_email(request , user , mail_subject , email_template)

            messages.success(request , 'reset password link has been sent to your email address')

            return redirect('login')
        else:
            messages.error(request , 'account does not exist')
            return redirect('forgot_password')
        

    return render(request , 'accounts/forgot_password.html')




def reset_password_validate(request , uidb64 , token):

    # validate the user by decoding the token and user pk

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except(ValueError , TypeError , OverflowError , CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user , token):
        request.session['uid'] = uid
        messages.info(request , 'please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request , 'this link has been expired')
        return redirect('myAccount')
    


def reset_password(request):

    if request.method == 'POST':

        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')

        uid = request.session.get('uid')
        if not uid:
            messages.error(request, 'Session expired. Please use the reset link again.')
            return redirect('forgot_password')

        try:
            user = CustomUser.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found. Please try again.')
            return redirect('forgot_password')

        

        # Clear uid from session for security
        request.session.pop('uid', None)

        messages.success(request, 'Your password has been reset successfully.')
        return redirect('login')

    return render(request, 'accounts/reset_password.html')



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
    orders = Order.objects.filter(custom_user=request.user , is_ordered=True).order_by('-created_at')
    recent_orders = orders[:5]
    context = {
        'orders':orders,
        'orders_count':orders.count(),
        'recent_orders':recent_orders,
    }
    return render(request , 'accounts/customerdashboard.html' , context)


@login_required
@user_passes_test(check_role_seller)
def sellerdashboard(request):
    seller = Seller.objects.get(custom_user=request.user)
    orders = Order.objects.filter(sellers=seller , is_ordered=True).order_by('-created_at')
    recent_orders = orders[:5]

    # total revenue
    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_seller()['grand_total']

    # current month revenue
    current_month_revenue = 0
    current_month = datetime.now().month
    current_month_orders = orders.filter(sellers=seller , created_at__month=current_month)

    for i in current_month_orders:
        current_month_revenue += i.get_total_by_seller()['grand_total']

    context = {
        'orders':orders,
        'orders_count':orders.count(),
        'recent_orders':recent_orders,
        'total_revenue':total_revenue,
        'current_month_revenue':current_month_revenue,
    }
    return render(request , 'accounts/sellerdashboard.html' , context)



'''
def reset_password(request):

    if request.method == 'POST':

        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = CustomUser.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request , 'password reset successful')
            return redirect('login')
        else:
            messages.error(request , 'password do not match')
            return redirect('reset_password')

    return render(request , 'accounts/reset_password.html')
'''







