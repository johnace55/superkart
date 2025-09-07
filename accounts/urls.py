from django.urls import path
from accounts import views


urlpatterns = [
    path('registercustomer/' , views.registercustomer , name='registercustomer'),
    path('registerseller/' , views.registerseller , name='registerseller'),
]






