from django.db.models import Q
from django.shortcuts import render
from shop.models import product

def search(request):
    b=None
    query=""
    if(request.method=="POST"):
        query=request.POST['s']
        if query:
            b=product.objects.filter(Q(name__icontains=query) | Q (price__icontains=query))   #django lookups

    return render(request,'search.html',{'product':b,'query':query})
