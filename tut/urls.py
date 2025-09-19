from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name='home'),
    path('product_detail/<slug:slug>/' , views.product_detail , name='product_detail'),
    
    path('seller_store/<str:store_name>/' , views.seller_store , name='seller_store'),

    path('all_products/' , views.all_products , name='all_products'),
    path('category/<str:category>/' , views.all_products , name='products_by_category'),

    
]




