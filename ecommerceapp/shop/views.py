from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from shop.models import category,product
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def categorys(request):
    c=category.objects.all()
    context={'cat':c}
    return render(request,'categorys.html',context)

def products(request,i):
    c=category.objects.get(id=i)
    p=product.objects.filter(category=c)
    context={'cat':c,'pro':p}
    return render(request,'products.html',context)

def productdetail(request,i):
    p=product.objects.get(id=i)
    context={'pro':p}
    return render(request,'productdetail.html',context)


def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        e = request.POST['e']
        f = request.POST['f']
        l = request.POST['l']
        if(p==cp):
            u=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
            u.save()
        else:
            return HttpResponse("password not same")
        return redirect('shop:categorys')

    return render(request,'register.html')



def userlogin(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']

        user=authenticate(username=u,password=p)

        if user:
            login(request,user)
            return redirect('shop:categorys')
        else:
            return HttpResponse("invalid credentials")

    return render(request,'login.html')

@login_required
def userlogout(request):
    logout(request)
    return redirect('shop:login')

def addcategories(request):
    if (request.method == "POST"):
        n= request.POST['n']
        d= request.POST['d']
        i = request.FILES['i']
        b =category.objects.create(name=n,description=d,image=i)
        b.save()
        return redirect('shop:categorys')

    return render(request,'addcategories.html')

def addproducts(request):
    if (request.method == "POST"):
        n= request.POST['n']
        d= request.POST['d']
        i = request.FILES.get('i')
        s=request.POST['s']
        p = request.POST['p']     # .get()
        c= request.POST['c']
        cat=category.objects.get(name=c)
        b =product.objects.create(name=n,desc=d,image=i,stock=s,price=p,category=cat)
        b.save()
        return redirect( 'shop:categorys')

    return render(request,'addproducts.html')

def addstock(request,i):
    a=product.objects.get(id=i)

    if(request.method=='POST'):
            a.stock=request.POST['a']
            a.save()
            return redirect('shop:productdetail',i)
    context = {'pro':a}
    return render(request,'addstock.html',context)





