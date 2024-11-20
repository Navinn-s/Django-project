
from cart.models import cart

def count(requets):
    count=0
    if requets.user.is_authenticated:
        u=requets.user
        c=cart.objects.filter(user=u)
        for i in c:
            count+=i.quantity
    return {'count':count}
