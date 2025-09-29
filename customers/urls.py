from django.urls import path
from customers import views
from accounts import views as accountviews

urlpatterns = [
    path('' , accountviews.customerdashboard , name='customerdashboard'),
    path('customerprofile/' , views.customer_profile , name='customerprofile'),
    path('customers_my_orders/' , views.customers_my_orders , name='customers_my_orders'),
    path('c_order_details/<str:order_number>/' , views.c_order_details , name='c_order_details'),
]
