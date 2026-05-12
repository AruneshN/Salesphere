from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Store

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