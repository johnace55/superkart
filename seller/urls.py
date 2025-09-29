from django.urls import path
from seller import views
from accounts import views as accountviews

urlpatterns = [
    path('' , accountviews.sellerdashboard , name='seller'),
    path('profile/' , views.seller_profile , name='seller_profile'),


    path('product_builder/' , views.product_builder , name='product_builder'),

    # CRUD PRODUCT
    path('product_builder/product/add_product/' , views.add_product , name='add_product'),
    path('product_builder/product/edit_product/<int:pk>/' , views.edit_product , name='edit_product'),
    path('product_builder/product/delete_product/<int:pk>/' , views.delete_product , name='delete_product'),


    path('s_order_details/<str:order_number>/' , views.s_order_details , name='s_order_details'),
    path('seller_my_orders/' , views.seller_my_orders , name='seller_my_orders'),
] 








