from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from . import forms
from .forms import Registeruser,Userstore,Productform,Customerform,Billform,Billitemform
from .models import Bill,Product,Customer,Billitem
from django.db.models import F,Sum
from datetime import date,timedelta
from django.utils import timezone


# Create your views here.

# index page
class index(TemplateView):
    template_name="index.html"
   
    def post(self,request,*args,**kwargs):
        user_name=request.POST.get("emp_id")
        user_password=request.POST.get("Password")

        user=authenticate(request,username=user_name,password=user_password)

        if user:
            login(request,user)
            return redirect('dashboard')
        else:
            return render(request,self.template_name,{'error':"login failed"})


class signup(TemplateView):
    template_name = "signup.html"

    def get(self, request, *args, **kwargs):
        register_form = Registeruser()
        store_form    = Userstore()
        return render(request, self.template_name, {
            "Register_user": register_form,   # instance, not class
            "user_store":    store_form,
        })

    def post(self, request, *args, **kwargs):
        register_form = Registeruser(request.POST)
        store_form    = Userstore(request.POST)
        if register_form.is_valid() and store_form.is_valid():
            user      = register_form.save()
            new_store = store_form.save(commit=False)
            new_store.user = user
            new_store.save()
            # return redirect("dashboard")
            return render (request,self.template_name,context={
                'success':True,
                 "Register_user": Registeruser(),  
            "user_store":    Userstore(),   
            })

        return render(request, self.template_name, {
            "Register_user": register_form,  
            "user_store":    store_form,      
        })


class dashboard(LoginRequiredMixin,TemplateView):
    template_name="dashboard.html"
    login_url='/'
      
    def get(self,request,*args,**kwargs):
        store=request.user.store
        total_products=Product.objects.count()
        total_customer=Customer.objects.count()
        total_bill=Bill.objects.count()
        

        # current month revenue
        date=timezone.now().date()
        this_month_bills=Bill.objects.filter(store=store,created_at__month=date.month,created_at__year=date.year)
        this_month_revenue=sum(bill.grand_total for bill in this_month_bills)

        # dashboard chart
        last_seven_days = timezone.now() - timedelta(days=7)
        week_data=Bill.objects.filter(created_at__gte=last_seven_days)
        data=[]
        for i in week_data:
            data.append(float(i.grand_total))

        # top selling Products:
    
        top_products=(Billitem.objects.values("product_name").annotate(total_sold=Sum("quantity")).order_by("-total_sold")) #top sold products    
        max_sold=top_products[0] ["total_sold"] if top_products else 1 # if no products sold return 0
        for products in top_products:
            products["percentage"]=(products["total_sold"] / max_sold)* 100 # calculate number of percentage

        return render(request,self.template_name,context={
            "total_products":total_products,
            "total_customer":total_customer,
            "total_bill":total_bill,
            "this_month_revenue":this_month_revenue,
            "week_sales_data":data,
            "week_total_amount": sum(data) if data else 0,
            "peek_day":max(data) if data else 0,
            "Avg_day":min(data) if data else 0,
            "top_products":top_products
        })


class add_product(LoginRequiredMixin,TemplateView):
    template_name="dashboard.html"
    login_url='/'
    
    def get(self,request,*args,**kwargs):
        productform=Productform()
        return render(request,self.template_name,context={
            "active_page":'dashboard',
            "productform":productform     
        })

    def post(self,request,*args,**kwargs):
        productform=Productform(request.POST)
        if productform.is_valid():
            product=productform.save(commit=False)
            product.store=request.user.store
            product.save()
            return render(request,self.template_name,context={
                "productform":Productform()
            })
        return render(request,self.template_name,context={
            "productform":productform,
        })

class add_customer(LoginRequiredMixin,TemplateView):
    template_name="dashboard.html"
    login_url='/'

    def get(self,request,*args,**kwargs):
        customerform=Customerform()
        return render(request,self.template_name,context={
            'active_page':'products',
            'customerform':customerform
        })
    def post(self,request,*args,**kwargs):
        customerform=Customerform(request.POST)
        if customerform.is_valid():
            customer=customerform.save(commit=False)
            customer.store=request.user.store
            customer.save()
            return render(request,self.template_name,context={
                "customerform":Customerform()
            })
        return render(request,self.template_name,context={
                "customerform":customerform
            })

# bill creation
def get_financial_year():
    today = date.today()
    if today.month >= 4:
        return f"{today.year}-{str(today.year + 1)[2:]}"
    else:
        return f"{today.year - 1}-{str(today.year)[2:]}"

def generate_bill_number(store):
    fy = get_financial_year()
    count = Bill.objects.filter(
        store=store,
        Bill_num__startswith=f"INV-{fy}"
    ).count() + 1
    return f"INV-{fy}/{count:04d}"


class createbill(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = '/'
    def get(self, request):
        return render(request, self.template_name, {
            'active_page': 'bills',
        })
    def post(self, request, *args, **kwargs):
        billform = Billform(request.POST)
        billitemform = Billitemform(request.POST)

        if billform.is_valid() and billitemform.is_valid():
            bill = billform.save(commit=False)
            bill.store = request.user.store
            bill.Bill_num = generate_bill_number(request.user.store)

            # bill status
            if "save_draft" in request.POST:
                bill.bill_status ="Drafts"
                print(request.POST)
            elif "create_bill" in request.POST:
                bill.bill_status ="Finalized"
                print(request.POST)

            bill.save()
            print("BILL SAVED:", bill.id, bill.Bill_num)

            billitem = billitemform.save(commit=False)
            billitem.bill = bill
            billitem.save()


            # product stock update after sell
            stock=Product.objects.get(id=billitem.product.id)
            stock.current_stock -=billitem.quantity
            stock.save()

            print("ITEM SAVED:", billitem.id)
            return redirect('dashboard')

        print("VALIDATION FAILED")
        return render(request, self.template_name, {
            "billform": billform,
            "billitemform": billitemform
        })
    
# ======================================= stock alert

class stock_alert(LoginRequiredMixin,TemplateView):
    template_name="dashboard.html"
    login_url='/'
    def get(self,request,*args,**kwargs):
        store=request.user.store
        # skus
        skus=Product.objects.filter(store=store).count()
        print(skus)
        return render(request,self.template_name,context={
                "active_page":"inventory",
                'skus':skus
            }
        )

class Allproducts(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    def get(self, request, *args, **kwargs):
        store = request.user.store
        products = list(
            Product.objects.filter(store=store).values(
                "id",
                "product_code",
                "product_name",
                "categories",
                "current_stock",
                "minimum_stock",
                "selling_price",
                "Tax",    
            )
        )
        return HttpResponse(products)

# payments
class payment(LoginRequiredMixin, TemplateView):
    
    template_name="dashboard.html"
    def get(self,request,*args,**kwargs):
        pending_bills = Bill.objects.filter(
    bill_status='Finalized',
).exclude(
    paid_amount__gt=0,  
).select_related('customer').order_by('due_date')
        
        # total bill amount

        total_bill=Bill.objects.exclude(bill_status__in=["Draft","Cancelled"]) #total bills without draft and canceled
        total_inv_amt=sum([total.grand_total for total in total_bill])#overall invoices amount
        inv_collected_amt=sum([collected_amt.paid_amount for collected_amt in total_bill]) #total collected invoice amounts
        unpaid_inv=len([
            unpaid_bill for unpaid_bill in total_bill
            if unpaid_bill.paid_amount <= unpaid_bill.grand_total
            
        ])# unpaid number of invoices


        return render(request,self.template_name,context=
                      {
                          "bills":pending_bills,
                          "total_inv_amt":total_inv_amt,
                          "Collected_amt":inv_collected_amt,
                          "unpaid_invoice":unpaid_inv
                      })

