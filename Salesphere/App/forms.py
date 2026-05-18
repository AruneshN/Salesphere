from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Store,Product,Customer,Bill,Billitem

class Registeruser(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name  = forms.CharField(max_length=50, required=True)
    email      = forms.EmailField(required=True)

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class Userstore(forms.ModelForm):
    class Meta:
        model  = Store
        fields = ['store_name', 'gst_number', 'address', 'category', 'mobile_number']


class Productform(forms.ModelForm):
    class Meta:
        model=Product
        fields = [
            'product_name', 'product_code', 'categories', 'brand',
            'description', 'purchase_price', 'selling_price', 'Tax',
            'opening_stock', 'minimum_stock', 'units'
        ]


class Customerform(forms.ModelForm):
    class Meta:
        model=Customer
        fields = [
    "name",
    "customer_type",
    "phone_number",
    "email",

    # Address
    "address",
    "city",
    "state",
    "pincode",
    "country",

    # Business & Tax info
    "gstin",
    "pan_number",
    "credit_limit",
    "payment_term",
]

    customer_type = forms.ChoiceField(
        choices=[("", "Select Customer Type...")] + Customer.CUSTOMER_TYPE
    )
    payment_term=forms.ChoiceField(
        choices=[("","Select Payment Terms...")]+Customer.PAYMENT_TERM
    )


class Billform(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=[("", "Select Payment Method")] + list(Bill._meta.get_field("payment_method").choices),
        required=False
    )
    class Meta:
        model=Bill
        fields = [
    "customer",
    "bill_date",
    "due_date",
    "notes",
    "payment_method",
]
   
        
class Billitemform(forms.ModelForm):
    class Meta:
        model=Billitem
        fields = [
    "product",
    "quantity",
    "unit_price",
    "tax",
]
        