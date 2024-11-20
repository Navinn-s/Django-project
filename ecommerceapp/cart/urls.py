
"""
URL configuration for ecommerceapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf.urls.static import static
from django.conf import settings
from cart import views
from django.urls import path
app_name="cart"


urlpatterns = [
    path('addtocart/<int:i>',views.addtocart, name='addtocart'),
    path('cartview',views.cartview,name='cartview'),
    path('minusfromcart/<int:i>',views.minusfromcart,name='minusfromcart'),
    path('delete/<int:i>',views.delete,name='delete'),
    path('orderform',views.orderform,name='orderform'),
    path('paymentstatus/<str:p>',views.payment_status,name='paymentstatus'),
    path('your_order',views.your_order,name='your_order')


]
