from django.contrib import admin

from .models import Product, Bid, Comment, Category, User

# Register your models here.
for model in [
    Product,
    Bid,
    Comment,
    Category,
    User,
]:
    admin.site.register(model)