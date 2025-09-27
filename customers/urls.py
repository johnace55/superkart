from django.urls import path
from customers import views
from accounts import views as accountviews

urlpatterns = [
    path('' , accountviews.customerdashboard , name='customerdashboard'),
    path('customerprofile/' , views.customer_profile , name='customerprofile'),
    path('customers_my_orders/' , views.customers_my_orders , name='customers_my_orders'),
    path('order_details/<str:order_number>/' , views.order_details , name='order_details'),
]
