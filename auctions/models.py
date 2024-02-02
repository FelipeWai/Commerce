from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category_name = models.CharField(max_length=64)

class AuctionsListing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=150)
    image_url = models.CharField(max_length = 400, blank=True, null=True)
    minimum_bid = models.IntegerField()
    is_open = models.BooleanField()

class Bids(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bid_Owner")
    price = models.IntegerField()
    auction_id = models.ForeignKey(AuctionsListing, on_delete=models.CASCADE)


class watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(AuctionsListing, on_delete=models.CASCADE)


class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comment_Owner")
    auction_id = models.ForeignKey(AuctionsListing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)