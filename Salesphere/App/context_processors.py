from .forms import Registeruser,Userstore,Productform,Customerform,Billform,Billitemform


def all_forms(request):
    if not request.user.is_authenticated:
        return {}  # ✅ skip for logged out users
    return {
        "productform": Productform(),
        "customerform": Customerform(),
        "billform":Billform(),
        "billitemform":Billitemform()
    }