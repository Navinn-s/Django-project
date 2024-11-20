from django.shortcuts import render,redirect
from cart.models import cart
from django.views.decorators.csrf import csrf_exempt
from shop.models import product
import razorpay
from cart.models import payment,orderdetails

def addtocart(request,i):
    p=product.objects.get(id=i)
    u=request.user

    try:
        c=cart.objects.get(user=u,product=p)
        print(c)
        c.quantity+=1
        p.stock-=1
        c.save()
        p.save()

    except:
        c=cart.objects.create(product=p,user=u,quantity=1)
        p.stock-=1
        c.save()
        p.save()

    return redirect('cart:cartview')


def cartview(request):
    u=request.user
    c=cart.objects.filter(user=u)

    total=0
    for i in c:
        total+=i.quantity*i.product.price
    context={'cart':c,'total':total}
    return render(request,'addtocart.html',context)

def minusfromcart(request,i):
    p = product.objects.get(id=i)
    u = request.user
    c=cart.objects.get(user=u,product=p)
    if(c.quantity>1):
        c.quantity-=1
        c.save()
        p.stock+=1
        p.save()

    else:
        c.delete()
        p.stock+=1
        p.save()
    return redirect('cart:cartview')

def delete(request,i):

    p = product.objects.get(id=i)
    u = request.user
    try:
        c = cart.objects.get(user=u, product=p)
        c.delete()
        p.stock += 1
        p.save()

    except:
        pass
    return redirect('cart:cartview')

# return render(request,'cart:cartview')

def orderform(request):
    if (request.method=='POST'):
        a=request.POST['a']
        pn=request.POST['p']
        n=request.POST['n']

        u=request.user
        c=cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.product.price*i.quantity


        #razorpay connection

        client=razorpay.Client(auth=('rzp_test_NglMD25PYAd74i','pFKb63vxczkx0QtPSwJDfAdK'))

        #razopay order creation

        response_payment=client.order.create(dict(amount=total*100,currency='INR'))

        order_id=response_payment['id']
        status=response_payment['status']
        if status=="created":
            p=payment.objects.create(name=u.username,amount=total,orderid=order_id)
            p.save()

            for i in c:
                o=orderdetails.objects.create(product=i.product,user=i.user,phone=pn,address=a,pincode=n,orderid=order_id)
                o.save()

            context={'payment':response_payment,'name':u.username}

            return render(request, 'payment.html',context)

    return render(request, 'orderform.html')


from django.contrib.auth.models import User
from django.contrib.auth import login
@csrf_exempt
def payment_status(request,p):
    user=User.objects.get(username=p)
    login(request,user)

    response=request.POST
    print(response)

    param_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],
    }

    client=razorpay.Client(auth=('rzp_test_NglMD25PYAd74i','pFKb63vxczkx0QtPSwJDfAdK'))
    try:
        status=client.utility.verify_payment_signature(param_dict)
        print(status)

        p=payment.objects.get(orderid=response['razorpay_order_id'])
        p.rezorpay_payment_method=response['razorpay_payment_id']
        p.paid=True
        p.save()

        o=orderdetails.objects.filter(orderid=response['razorpay_order_id'])
        for i in o:
            i.paymentstatus='completed'
            i.save()

        c=cart.objects.filter(user=user)
        c.delete()

    except:
        pass

    return render(request,'paymentstatus.html')

def your_order(request):
    u=request.user
    o=orderdetails.objects.filter(user=u,paymentstatus='completed')
    context={'order':o}
    return render(request,'your_order.html',context)