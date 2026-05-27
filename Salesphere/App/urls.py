from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
   
    path('',views.index.as_view(),name="index"),
    path('src/',views.src.as_view(),name="index"),
    path('dashboard/',views.dashboard.as_view(),name="dashboard"),
    path('signup/',views.signup.as_view(),name="signup"),
    path('add_product/',views.add_product.as_view(),name="add-new-product"),
    path("add_customer/",views.add_customer.as_view(),name="add-customer"),
    path("create_bill/",views.createbill.as_view(),name="create-bill"),
    path("stock_alert/",views.stock_alert.as_view(),name="stock-alert"),
    path("allstocks/",views.Allproducts.as_view())

]
