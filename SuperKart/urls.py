"""
URL configuration for SuperKart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('cart/' , include('product.urls')),

    path('accounts/' , include('accounts.urls')),

    path('' , include('tut.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 

from django.conf.urls import handler403
from django.shortcuts import render

def custom_permission_denied_view(request, exception=None):
    return render(request, "accounts/403.html", status=403)

handler403 = custom_permission_denied_view



