from django.db import models

from shop.models import product
from django.contrib.auth.models import User


class cart(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    quantity= models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)


    def subtotal(self):
        return self.product.price*self.quantity


    def __str__(self):
        return self.product.name

class orderdetails(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.TextField()
    phone=models.BigIntegerField()
    pincode=models.IntegerField()

    orderid=models.CharField(max_length=30)
    paymentstatus=models.CharField(max_length=30,default='pending')
    delivarystatus=models.CharField(max_length=30,default='pending')
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.orderid

class payment(models.Model):
    name=models.CharField(max_length=30)
    amount=models.IntegerField()
    orderid=models.CharField(max_length=30)
    rezorpay_payment_method=models.CharField(max_length=30,blank=True)
    paid=models.BooleanField(default=False)


    def __str__(self):
        return self.orderid