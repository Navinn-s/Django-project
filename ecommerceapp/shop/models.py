from django.db import models


class category(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    image=models.ImageField(upload_to='category')

    def __str__(self):
        return self.name

class product(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='products')
    desc=models.TextField()
    price=models.IntegerField()
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    category=models.ForeignKey(category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name



