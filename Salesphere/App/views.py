from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from . import forms
from .forms import Registeruser,Userstore,Productform,Customerform,Billform,Billitemform
from .models import Bill,Product
from django.db.models import F
from datetime import date

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

class add_product(LoginRequiredMixin,TemplateView):
    template_name="dashboard.html"
    login_url='/'

    def get(self,request,*args,**kwargs):
        productform=Productform()
        return render(request,self.template_name,context={
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
    def post(self, request, *args, **kwargs):
        billform = Billform(request.POST)
        billitemform = Billitemform(request.POST)
        
        # print("POST DATA:", request.POST)
        # print("BILL VALID:", billform.is_valid())
        # print("BILL ERRORS:", billform.errors)
        # print("ITEM VALID:", billitemform.is_valid())
        # print("ITEM ERRORS:", billitemform.errors)

        if billform.is_valid() and billitemform.is_valid():
            bill = billform.save(commit=False)
            bill.store = request.user.store
            bill.Bill_num = generate_bill_number(request.user.store)
            bill.save()
            print("BILL SAVED:", bill.id, bill.Bill_num)

            billitem = billitemform.save(commit=False)
            billitem.bill = bill
            billitem.save()
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
        
        # out_of_stock - current stock is 0
        out_of_stock=Product.objects.filter(store=store,current_stock=0)

        #warning stock current stock is +5 than minimum stock
        warning_stock=Product.objects.filter(store=store,current_stock__gt=F("minimum_stock"),current_stock__lte=F("minimum_stock")+5)

        #low stock
        low_stock=Product.objects.filter(store=store,current_stock__gt=0,current_stock__lte=F("minimum_stock"))

        return render(request,self.template_name,context={
                "out_of_stock":out_of_stock,
                "warning_stock":warning_stock,
                "low_stock":low_stock
            }
        )
        