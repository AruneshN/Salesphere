from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
   
    path('',views.index.as_view(),name="index"),
    path('dashboard/',views.dashboard.as_view(),name="dashboard"),
    path('signup/',views.signup.as_view(),name="signup"),
    path('add_product/',views.add_product.as_view(),name="add-new-product"),
    path("add_customer/",views.add_customer.as_view(),name="add-customer"),
    path("create_bill/",views.createbill.as_view(),name="create-bill"),
    path("invoice_view/<int:pk>/",views.invoice_view.as_view(),name="view_invoice"),
    path("stock_alert/",views.stock_alert.as_view(),name="stock-alert"),
    path("stock/update/<int:product_id>/", views.update_stock, name="update-stock"),
    path("allstocks/",views.Allproducts.as_view()),
    path("payments/",views.payment.as_view(),name="invoice-payment"),
path('payment_collect/<int:invoice_id>/', views.collect_payment, name='collect-payment'),
path('payment_undo/<int:invoice_id>/',    views.undo_payment,    name='undo-payment'),
    path('payment_edit/<int:invoice_id>/',    views.edit_payment,    name='edit-payment'),


]
