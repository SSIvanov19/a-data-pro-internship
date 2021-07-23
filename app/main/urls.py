from django.urls import path
from . import views

urlpatterns = [
path("", views.home, name="home"),
path("home/", views.home, name="home"),
path("account/", views.account, name="account"),
path("scraper/", views.scraper, name="scraper"),
path('registerPage/', views.registerPage, name="registerPage"),
path('loginPage/', views.loginPage, name="loginPage"),  
]

