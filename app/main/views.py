from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from django.contrib import messages
from .models import *
from .forms import CreateUserForm

# Create your views here.


def home(response):
    return render(response, "main/home.html", {})

def account(response):
    return render(response, "main/account.html", {})

def crawler(response):
    return render(response, "main/crawler.html", {})

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('loginPage')
			

		context = {'form':form}
		return render(request, 'main/registerPage.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'main/loginPage.html', context)

