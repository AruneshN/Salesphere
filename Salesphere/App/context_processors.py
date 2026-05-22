from .forms import Registeruser,Userstore,Productform,Customerform,Billform,Billitemform
from .models import Product,Bill
from django.db.models import F
from django.utils import timezone
from itertools import chain
 

def all_forms(request):
    if not request.user.is_authenticated:
        return {}  #skip for logged out users
    
    skus=Product.objects.count()

    store=request.user.store
        
    # out_of_stock - current stock is 0
    out_of_stock=Product.objects.filter(store=store,current_stock=0)
    total_out_of_stock=out_of_stock.count()

    #warning stock current stock is +5 than minimum stock
    warning_stock=Product.objects.filter(store=store,current_stock__gt=F("minimum_stock"),current_stock__lte=F("minimum_stock")+5)
    total_warning_stock=warning_stock.count()

    #low stock
    low_stock=Product.objects.filter(store=store,current_stock__gt=0,current_stock__lte=F("minimum_stock"))
    total_low_stock=low_stock.count()

    total=total_out_of_stock+total_warning_stock+total_low_stock
    low_stock_total=total_warning_stock + total_low_stock # low stock + warning stock

    # healthy stock
    healthy_stock=Product.objects.filter(store=store,current_stock__gt=F("minimum_stock")+5)
    total_healthy_stock=healthy_stock.count()

    stock_alert=list(chain(
        out_of_stock,
        warning_stock,
        low_stock
    ))
    # minimum stock of the product


    # ================================ today bills and sales ===========================
    today=timezone.now().date()

    # quaryset for bills
    today_bills=Bill.objects.filter(created_at__date=today)

    #today bills
    today_bill_count=Bill.objects.filter(created_at__date=today).count()

    #today revenue
    today_revenue=sum(today_revnues.grand_total for today_revnues in today_bills)
    return {
        "productform": Productform(),
        "customerform": Customerform(),
        "billform":Billform(),
        "billitemform":Billitemform(),

        #stock data
        'skus':skus,
        # out of stock
        "out_of_stock":out_of_stock,
        "total_out_of_stock":total_out_of_stock,

        # warning stock
        "warning_stock":warning_stock,
        "total_warning_stock":total_warning_stock,
        
        #low stock 
        "low_stock":low_stock,
        "total_low_stock":total_low_stock,

        # healthy stock
        "total_healthy_stock":total_healthy_stock,

        "stock_alert":stock_alert,
        
        #total bills 
        "total":total,

        # total low stock
        "low_stock_total":low_stock_total,

        #today bill count
        "today_bill_count":today_bill_count,

        # today revenue
        "today_revenue":today_revenue


    }