from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views.generic import TemplateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from . import forms
from .forms import Registeruser,Userstore,Productform,Customerform,Billform,Billitemform
from .models import Bill,Product,Customer,Billitem
from django.db.models import F,Sum
from datetime import date,timedelta
from django.utils import timezone
import json
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

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



class add_customer(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = '/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)  # ✅ context processor handles everything

    def post(self, request, *args, **kwargs):
        customerform = Customerform(request.POST)
        print("FORM ERRORS:", customerform.errors)

        if customerform.is_valid():
            customer = customerform.save(commit=False)
            customer.store = request.user.store
            customer.save()
            print("✅ Customer saved:", customer.id)
            return redirect('add-customer')
        
        print("❌ Not saved")
        return redirect('add-customer')  # ✅ always redirect — context processor re-runs on GET


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



# ==================================== invoice views
class invoice_view(LoginRequiredMixin,DetailView):
    model=Bill
    template_name="invoice_view.html"
    context_object_name="invoice_data"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["store"]=self.request.user.store
        context["items"]=self.object.billitem_set.all()
        return context


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
    def post(self,request,*args,**kwargs):
        data = json.loads(request.body)
        Products=Product.objects.get(sku=data['sku'])
        breakpoint()

@login_required
@require_http_methods(["POST","DELETE"])
def update_stock(request,product_id):
    try:
        product=Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Product not found'}, status=404)
 
    if request.method == "DELETE":
        product.delete()
        return JsonResponse({'ok': True})

    try:
        data=json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'Invalid JSON'}, status=400)
    
    if 'name'  in data: product.product_name  = data['name']
    if 'sku'   in data: product.product_code   = data['sku']
    if 'qty'   in data: product.current_stock  = int(data['qty'])
    if 'min'   in data: product.minimum_stock  = int(data['min'])
    if 'price' in data: product.selling_price  = float(data['price'])
    product.save()
    return JsonResponse({'ok': True, 'id': product.id})


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

@login_required
@require_http_methods(["POST"])
def collect_payment(request, invoice_id):
    try:
        data        = json.loads(request.body)
        amount_paid = float(data.get('amount_paid', 0))
        method      = data.get('method', 'Cash')

        invoice = Bill.objects.get(id=invoice_id)

        if amount_paid <= 0:
            return JsonResponse({'ok': False, 'error': 'Amount must be greater than 0'})
        if amount_paid > float(invoice.grand_total):
            return JsonResponse({'ok': False, 'error': 'Amount exceeds invoice total'})

        invoice.paid_amount    = amount_paid
        invoice.payment_method = method
        invoice.save()

        return JsonResponse({
            'ok':             True,
            'paid_amount':    float(invoice.paid_amount),
            'payment_status': invoice.payment_status,  # ✅ read it, don't set it
            'payment_method': invoice.payment_method,
        })

    except Bill.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Invoice not found'}, status=404)
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def undo_payment(request, invoice_id):
    try:
        invoice = Bill.objects.get(id=invoice_id)
        
        invoice.paid_amount    = 0
        invoice.payment_method = 'Cash'
        invoice.save()

        return JsonResponse({
            'ok':             True,
            'paid_amount':    float(invoice.paid_amount),
            'payment_status': invoice.payment_status,  # read-only property
            'payment_method': invoice.payment_method,
        })

    except Bill.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Invoice not found'}, status=404)
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)
    

@login_required
@require_http_methods(["POST"])
def edit_payment(request, invoice_id):
    try:
        data     = json.loads(request.body)
        total    = float(data.get('total', 0))
        paid     = float(data.get('paid', 0))
        method   = data.get('method', 'Cash')
        due_date = data.get('due_date', None)

        if total <= 0:
            return JsonResponse({'ok': False, 'error': 'Total must be greater than 0'})
        if paid > total:
            return JsonResponse({'ok': False, 'error': 'Paid amount cannot exceed total'})
        if paid < 0:
            return JsonResponse({'ok': False, 'error': 'Paid amount cannot be negative'})

        invoice = Bill.objects.get(id=invoice_id)

        # invoice.grand_total    = total
        invoice.paid_amount    = paid
        invoice.payment_method = method

        if due_date:
            from datetime import datetime
            invoice.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

        invoice.save()

        return JsonResponse({
            'ok':             True,
            'paid_amount':    float(invoice.paid_amount),
            'grand_total':    float(invoice.grand_total),
            'payment_status': invoice.payment_status,  # read-only property
            'payment_method': invoice.payment_method,
            'due_date':       str(invoice.due_date),
        })

    except Bill.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Invoice not found'}, status=404)
    except ValueError as e:
        return JsonResponse({'ok': False, 'error': 'Invalid date format: ' + str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)