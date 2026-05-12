from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
   
    path('',views.index.as_view(),name="index"),
    path('dashboard/',views.dashboard.as_view(),name="dashboard"),
    path('signup/',views.signup.as_view(),name="signup")
    
]
