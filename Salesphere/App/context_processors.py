from .forms import Registeruser,Userstore,Productform,Customerform,Billform,Billitemform
from .models import Product

def all_forms(request):
    if not request.user.is_authenticated:
        return {}  #skip for logged out users
    
    skus=Product.objects.count()
    return {
        "productform": Productform(),
        "customerform": Customerform(),
        "billform":Billform(),
        "billitemform":Billitemform(),

        #stock data
    
        'skus':skus
    }