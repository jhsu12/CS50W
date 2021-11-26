from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Auction(models.Model):
    #check date_posted
    seller = models.CharField(max_length=100, default="Test")
    date_posted = models.DateField(auto_now_add=True)

    title = models.TextField(max_length=100)
    description = models.TextField()
    start_bid = models.IntegerField()
    image = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='goods', default="None")
    
    current_bid = models.IntegerField(default=-1)
    buyer = models.CharField(max_length=100, blank=True)
    on_list = models.BooleanField(default=True)

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    lists = models.ForeignKey(Auction, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField()
    auction_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    