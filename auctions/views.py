from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Product, Category
from .forms.listing import Listing


def index(request):
    category = request.GET.get("category")
    activeList = Product.objects.all()
    if category is not None:
        activeList = activeList.filter(category=category)
    return render(request, "auctions/index.html", {
        "activeList": activeList
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createlist(request):
    form = Listing(request.POST or None)
    if form.is_valid():
        p = Product(
            **form.cleaned_data,
            owner=request.user
        )
        p.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/createlist.html", {
        "form": form
    })

def listingpage(request, product_id):
    print(Product.objects.get(pk=product_id))
    return render(request, "auctions/listingpage.html", {
        "product": Product.objects.get(pk=product_id)
    })

def watchlist(request):
    pass

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })