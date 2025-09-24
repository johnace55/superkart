from django.urls import path
from customers import views
from accounts import views as accountviews

urlpatterns = [
    path('' , accountviews.customerdashboard , name='customerdashboard'),
    path('customerprofile/' , views.customer_profile , name='customerprofile'),
]
