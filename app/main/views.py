from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .models import (
    Products,
    Pricesforeachstore,
    Linkforeachproductinstore,
    UsersSubscriptions,
)
from .tokens import account_activation_token
from .forms import CreateUserForm
from mysite import settings
from multiprocessing import Pool

# Create your views here.

from crawler_files.crawler_files.startCrawling import startCrawling


def home(response):
    return render(response, "main/index.html", {})


def account(request):
    if not request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            deleteAccount = request.POST.get("delete_account")

            user = request.user

            if deleteAccount == "true":
                user.delete()
                logout(request)
                return redirect("home")

            if username is not None and username != "":
                user.username = username

            if email is not None and email != "":
                user.email = email

            if password is not None and password != "":
                user.set_password(password)

            user.save()

        products = UsersSubscriptions.objects.filter(userid=request.user)

    return render(request, "main/account.html", {"products": products})


def scraper(request):
    # Get the product name from the url
    productName = request.GET.get("product_name")
    startScrapy = request.GET.get("start_scrapy")
    table = None

    if startScrapy == "true" and productName is not None and productName != "":
        try:
            pool = Pool(processes=1)
            pool.apply_async(startCrawling, [productName])
            pool.close()
        except Exception as e:
            print(e)

    # Check if product name is not empty
    if productName is not None and productName != "":
        table = Products.objects.filter(productname__icontains=productName)
        context = {"table": table, "search": productName}
    else:
        context = {"table": table}

    return render(request, "main/scraper.html", context=context)


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def productStats(request):
    # Get the product name from the url
    productNumber = request.GET.get("product_number")

    # Check if product name is not empty
    if productNumber is None or productNumber == "":
        return redirect("scraper")

    # Get the product from the database
    product = Products.objects.get(productnumber=productNumber)
    # Get the prices for the product from the database
    prices = Pricesforeachstore.objects.filter(productid=product.id)
    # Get the links for the product from the database
    links = Linkforeachproductinstore.objects.filter(productid=product.id)
    # Sort the prices
    prices = list(prices)
    prices.sort(key=lambda x: x.price)
    # Add link to each store
    for p in prices:
        p.price = truncate(p.price, 2)
        p.link = links.filter(storeid=p.storeid.id)[0].link

    products = None
    if request.user.is_authenticated:
        products = UsersSubscriptions.objects.filter(userid=request.user)

        print(request.user.is_authenticated)

        isSubscribe = False

        for p in products:
            if p.productId.id == product.id:
                isSubscribe = True

    context = {"product": product, "prices": prices, "isSubscribe": isSubscribe}

    if request.method == "POST":
        productNumber = request.POST.get("product_number_to_subscribe")
        usersSubscriptions = UsersSubscriptions.objects.create(
            userid=request.user,
            productId=product,
            isAvaible=True,
            Price=prices[0].price,
        )
        usersSubscriptions.save()
        messages.success(request, "Абонирахте се за този продукт")

    return render(request, "main/productStats.html", context=context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect("account")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                messages.success(
                    request, "Моля, потвърдете вашия акаунт, преди да продължите!"
                )

                user = form.save(commit=False)
                user.is_active = False
                user.save()
                currentSite = get_current_site(request)
                mailSubject = "Активация на вашия акаунт."
                message = render_to_string(
                    "main/verification_email_template.html",
                    context={
                        "user": user,
                        "domain": currentSite.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )
                toEmail = form.cleaned_data.get("email")
                send_mail(
                    subject=mailSubject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[toEmail],
                    html_message=message,
                )
                return redirect("loginPage")

        context = {"form": form}
        return render(request, "main/registerPage.html", context)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(
            "Благодарим, че си потвърдихте профила. Сега може да влезете в нашия уебсайт."
        )
    else:
        return HttpResponse("Активациония линк е невалиден!")


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("account")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Потребителското име и/или парола не са верни")

        context = {}
        return render(request, "main/loginPage.html", context)


def logoutUser(request):
    logout(request)
    return redirect("loginPage")
