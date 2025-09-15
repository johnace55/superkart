from django.urls import path
from seller import views
from accounts import views as accountviews

urlpatterns = [
    path('' , accountviews.sellerdashboard , name='seller'),
    path('profile/' , views.seller_profile , name='seller_profile'),
]



