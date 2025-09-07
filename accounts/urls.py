from django.urls import path
from accounts import views


urlpatterns = [
    path('registercustomer/' , views.registercustomer , name='registercustomer'),
    path('registerseller/' , views.registerseller , name='registerseller'),
    path('login/' , views.login , name='login'),
    path('logout/' , views.logout , name='logout'),
    
    path('myAccount/' , views.myAccount , name='myAccount'),

    path('sellerdashboard/' , views.sellerdashboard , name='sellerdashboard'),
    path('customerdashboard/' , views.customerdashboard , name='customerdashboard'),
]






