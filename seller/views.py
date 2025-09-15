from django.shortcuts import render , HttpResponse

# Create your views here.

def seller_profile(request):
    return render(request , 'seller/seller_prolfile.html')



