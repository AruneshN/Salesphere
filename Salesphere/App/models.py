from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP

# Create your models here.

# ========================================================= Store
class Store(models.Model): 

    class business_category(models.TextChoices):
        Grocery_market="Grocery / Supermarket"
        Electronic="Electronics & Appliances"
        Fashion="Clothing & Fashion"
        Pharmacy="Pharmacy / Medical"
        Food="Restaurant / Food"
        Hardware="Hardware / Tools"
        Books="Books / Stationery"
        Other="Other"


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="store")   
    store_name=models.CharField(blank=False,max_length=150)
    gst_number=models.CharField(max_length=20,unique=True,blank=True)
    address=models.TextField(blank=False)
    category=models.CharField(blank=False,max_length=30,choices=business_category.choices)
    mobile_number=models.CharField(blank=False,max_length=16)

    def __str__(self):
        return self.store_name
# ======================================================= store end
#========================================================= product category 
class category(models.Model): #product category 
    name=models.CharField(max_length=100)
    is_default=models.BooleanField(default=False)

    # def __str__(self):
    #     return self.name

# Add product
class Product(models.Model):
    TAX_CHOICES=[
        ("0","0% Exempt"),
        ("5","5% GST"),
        ("12","12% GST"),
        ("18","18% GST"),
        ("28","28% GST"),
    ]

    UNITS=[
        ("PCS","Pieces (Pcs)"),
        ("KG","Kilograms (Kg)"),
        ("L","Litres (L)"),
        ("Box","BOX"),
        ("Pack","Pack")
    ]

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    store=models.ForeignKey(Store,on_delete=models.CASCADE,related_name="Products")
    product_name=models.CharField(null=False,blank=False,max_length=120)
    product_code=models.CharField(max_length=120)
    categories=models.ForeignKey(category,on_delete=models.SET_NULL,null=True,related_name="products")
    brand=models.CharField(max_length=120) #brand/manufacture
    description=models.TextField()

    # price and stock
    purchase_price=models.DecimalField(max_digits=12,decimal_places=2)
    selling_price=models.DecimalField(max_digits=12,decimal_places=2)
    Tax=models.CharField(max_length=12,choices=TAX_CHOICES,default="18")
    opening_stock=models.DecimalField(max_digits=12,decimal_places=2)
    minimum_stock=models.DecimalField(max_digits=12,decimal_places=2)
    current_stock=models.DecimalField(max_digits=12,decimal_places=2)
    units=models.CharField(max_length=120,choices=UNITS,default="PCS")

    def __str__(self):
        return self.product_name
    

# ========================================================= Product END

# ======================================================== Customer 
class Customer(models.Model):
    CUSTOMER_TYPE=[
        ("Individual","Individual"),
        ("Business / Firm","Business / Firm"),
        ("Wholesale","Wholsesale"),
        ("Retailer","Retailer")
    ]

    PAYMENT_TERM=[
        ("Immediate","Immediate"),
        ("Net 7 days","Net 7 days"),
        ("Net 15 days","Net 15 days"),
        ("Net 30 days","Net 30 days")
    ]

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    store=models.ForeignKey(Store,on_delete=models.CASCADE,related_name="Customers")

    # contact details
    name=models.CharField(max_length=120,blank=False)
    customer_type=models.CharField(max_length=120,choices=CUSTOMER_TYPE)
    phone_number=models.CharField(max_length=15,blank=False,unique=True)
    email=models.EmailField(max_length=120)

    # Address
    address=models.TextField()
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=120)
    pincode=models.CharField(max_length=120)
    country=models.CharField(max_length=120)

    # Business & Tax info
    gstin=models.CharField(max_length=20)
    pan_number=models.CharField(max_length=20)
    credit_limit=models.DecimalField(max_digits=12,decimal_places=2)
    payment_term=models.CharField(max_length=30,choices=PAYMENT_TERM)

    def __str__(self):
        return self.name

# ================================================= Customer end

# ================================================= bill ======================
class Bill(models.Model):
    BILL_STATUS = [
    ("Draft", "Draft"),
    ("Finalized", "Finalized"),
    ("Cancelled", "Cancelled"),
]
    PAYMENT_METHODS=[
        ("Cash","Cash"),
        ("UPI","UPI"),
        ("Bank Transfer","Bank Transfer"),
        ("Credit","Credit")
    ]
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    store=models.ForeignKey(Store,on_delete=models.CASCADE)
    Bill_num=models.CharField(max_length=30,unique=True)
    customer=models.ForeignKey(Customer,blank=False,on_delete=models.PROTECT,related_name="Bills")
    bill_date=models.DateField(default=timezone.now)
    due_date=models.DateField(default=timezone.now)
    bill_status=models.CharField(max_length=20,choices=BILL_STATUS,default="Draft")
    paid_amount=models.DecimalField(max_digits=12,decimal_places=2,default=0)

    # line items
    notes=models.CharField(max_length=300,blank=True)
    payment_method=models.CharField(max_length=30,choices=PAYMENT_METHODS)

    def __str__(self):
        return f'BIll {self.Bill_num} - {self.store}'
    
    
    @property
    def payment_status(self):
        if self.bill_status == "Draft":
            return "Draft"

        today = timezone.now().date()

        # Fully paid
        if self.paid_amount >= self.grand_total:
            return "Paid"

        # Partial payment
        elif self.paid_amount > 0:
            return "Partial"

        # Overdue unpaid invoice
        elif self.due_date < today:
            return "Overdue"

        # No payment yet
        return "Pending"

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.billitem_set.all())

    @property
    def subtotal(self):
        total = sum(item.line_subtotal for item in self.billitem_set.all())
        return Decimal(total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def total_tax(self):
        total = sum(item.tax_amount for item in self.billitem_set.all())
        return Decimal(total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def grand_total(self):
        total = self.subtotal + self.total_tax
        return Decimal(total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class Billitem(models.Model):
    TAX_CHOICES=[
        ("0","0% Exempt"),
        ("5","5% GST"),
        ("12","12% GST"),
        ("18","18% GST"),
        ("28","28% GST"),
    ]
    bill=models.ForeignKey(Bill,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    #product name
    product_name=models.CharField(max_length=120,blank=True) 
    quantity=models.DecimalField(max_digits=12,decimal_places=2)
    unit_price=models.DecimalField(max_digits=12,decimal_places=2)
    tax=models.CharField(max_length=12,choices=TAX_CHOICES)

    def __str__(self):
        return f'{self.product.product_name} x {self.quantity} '
    
    def save(self,*args,**kwargs):
        if self.product:
            self.product_name=self.product.product_name
        super().save(*args,**kwargs)

    @property
    def line_subtotal(self):
        line_subtotal= self.unit_price * self.quantity
        return Decimal(line_subtotal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def tax_amount(self):
        from decimal import Decimal
        tax=self.line_subtotal * (Decimal(self.tax) / 100)
        return Decimal(tax).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def line_total(self):
        line_total=self.line_subtotal + self.tax_amount
        return Decimal(line_total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


