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
    image_url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}:{self.name} belongs to {self.category} category with price of {self.current_price}"

class Bid(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bids")
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user_name} bid {self.amount} on {self.product_id}"

class Comment(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.user_name} commented {self.comment} about {self_product_id}"

class Watchlist(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="watchers")
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user_name} watching {self.product_id}"
