from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    created_date = models.DateTimeField(auto_now_add=True)
    open = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"\n Product Name: {self.name} \n Category: {self.category} \n Start Bid: {self.current_price} "


class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} bid {self.amount} on {self.product_id}"


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.user} commented {self.comment}"


class Watchlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="watchers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user} watching {self.product_id}"
