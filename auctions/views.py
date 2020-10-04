from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms.listing import Listing
from .models import User, Product, Category, Watchlist, Bid, Comment


def is_watching(user, product):
    if not user.is_authenticated:
        return False

    watch_list = Watchlist.objects.filter(product=product, user=user)
    return bool(len(watch_list))


def get_winner(product):
    maxbid = Bid.objects.filter(product=product).aggregate(max=models.Max("amount"))["max"]
    winner = Bid.objects.filter(product=product, amount=maxbid)
    if len(winner):
        return winner.user
    else:
        return None


def get_title(**kwargs):
    if kwargs["category"]:
        return "Active Listings: " + Category.objects.get(id=kwargs["category"]).name
    if kwargs["closed"]:
        return "Closed Listings"

    return "Active Listings"


def index(request):
    category = request.GET.get("category")
    closed = bool(request.GET.get("closed"))
    active_list = Product.objects.filter(open=not closed).order_by('-created_date')
    if category is not None:
        active_list = active_list.filter(category=category)
    return render(request, "auctions/index.html", {
        "title": get_title(category=category, closed=closed),
        "activeList": active_list,

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
    product = Product.objects.get(pk=product_id)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add-watchlist":
            w = Watchlist(product=product, user=request.user)
            w.save()
        elif action == "remove-watchlist":
            Watchlist.objects.filter(product=product, user=request.user).delete()
        elif action == "place-bid":
            amount = float(request.POST.get("bidamount"))
            b = Bid(product=product, user=request.user, amount=amount)
            b.save()
            product.current_price = amount
            product.save()
        elif action == "close-listing":
            product.winner = get_winner(product)
            product.open = False
            product.save()
        elif action == "add-comment":
            c = Comment(product=product, user=request.user, comment=request.POST["comment"])
            c.save()
    comments = Comment.objects.filter(product=product)
    return render(request, "auctions/listingpage.html", {
        "product": product,
        "is_watching": is_watching(request.user, product),
        "comments": comments
    })


def watchlist(request):
    watch_list = Watchlist.objects.select_related("product").filter(user=request.user)
    active_list = list(map(lambda item: item.product, watch_list))
    return render(request, "auctions/index.html", {
        "title": "Your Watchlist",
        "activeList": active_list
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })
