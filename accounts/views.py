from django.shortcuts import render , redirect
from accounts.forms import CustomerForm
from accounts.models import CustomUser
from django.contrib import messages



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

 




