from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from . import forms
from .forms import Registeruser,Userstore
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

