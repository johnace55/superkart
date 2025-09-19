from django.urls import path
from product import views

urlpatterns = [
    path('' , views.cart , name='cart'),
    path('add_to_cart/<int:food_id>/' , views.add_to_cart , name='add_to_cart'),
    path('decrease_cart/<int:food_id>/' , views.decrease_cart , name='decrease_cart'),
    path('remove_cart/<int:food_id>/' , views.remove_cart , name='remove_cart'),
]





