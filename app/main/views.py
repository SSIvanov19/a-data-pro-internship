from django.shortcuts import render
from django.http import HttpResponse, request
from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from .models import Products, Pricesforeachstore, Linkforeachproductinstore, Stores
from .forms import CreateUserForm
# Create your views here.


def home(response):
    return render(response, "main/home.html", {})


def account(request):
	if not request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			email = request.POST.get('email')
			password =request.POST.get('password')
			deleteAccount = request.POST.get('delete_account')
			
			user = request.user

			if deleteAccount == 'true':
				user.delete()
				logout(request)
				return redirect('home')

			if username != None and username != '':
				user.username = username
			
			if email != None and email != '':
				user.email = email
			
			if password != None and password != '':
				user.set_password(password)
			
			user.save()

	return render(request, "main/account.html", {})


def scraper(request):
	#Get the product name from the url
	productName = request.GET.get('product_name')
	table = None
	
	#Check if product name is not empty
	if productName != None and productName != '':
		table = Products.objects.filter(productname__icontains=productName)
	context = {'table': table}
	return render(request, "main/scraper.html", context=context)

def productStats(request):
	#Get the product name from the url
	productNumber = request.GET.get('product_number')

	#Check if product name is not empty
	if productNumber == None or productNumber == '':
		return render(request, "main/scraper.html", {})

	#Get the product from the database
	product = Products.objects.get(productnumber=productNumber)
	#Get the prices for the product from the database
	prices = Pricesforeachstore.objects.filter(productid=product.id)
	#Get the links for the product from the database
	links = Linkforeachproductinstore.objects.filter(productid=product.id)
	#Sort the prices
	prices = list(prices)
	prices.sort(key=lambda x: x.price)
	#Add link to each store
	for p in prices:
		p.link = links.filter(storeid = p.storeid.id)[0].link

	context = {'product': product, 'prices': prices}
	return render(request, "main/productStats.html", context=context)

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
				messages.info(request, 'Username or password is incorrect')

		context = {}
		return render(request, 'main/loginPage.html', context)



def logoutUser(request):
	logout(request)
	return redirect('loginPage')


