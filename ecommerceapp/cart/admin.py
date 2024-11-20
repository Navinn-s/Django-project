from django.contrib import admin

from cart.models import cart,orderdetails,payment

admin.site.register(cart)
admin.site.register(orderdetails)
admin.site.register(payment)
