from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlist", views.createlist, name="createlist"),
    path("listingpage/<int:product_id>", views.listingpage, name="listingpage"),
    path("watchist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories")
]
