from django.urls import path
from . import views

urlpatterns = [
path("", views.home, name="home"),
path("home/", views.home, name="home"),
path("account/", views.account, name="account"),
path("crawler/", views.crawler, name="crawler"),
path('registerPage/', views.registerPage, name="registerPage"),
path('loginPage/', views.loginPage, name="loginPage"),  
]

