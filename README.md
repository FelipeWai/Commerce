# **CS50 Web project 2**

<br>

# Features
<ul>
    <li> Django </li>
    <li> Html </li>
    <li> Css </li>
    <li> JavaScript </li>
</ul>

<br>

# Project Description

### This project is a auction website where the users can list their auctions, can place bids, add auctions to their watchlist and make comments in the auctions page

<br>

# Database

### The database used was the SQLITE that comes with django

## The models:

### User model:
This was already in the project from the beggining so the "AbstractUser" was used. The "AbstractUser" has basic fields like email, username, password and etc.

```
class User(AbstractUser):
    pass
```


### Categories model:
This model has just the fild for the category name that's going to be used in other parts of the project
```
class Categories(models.Model):
    category_name = models.CharField(max_length=64)
```

### Auctions model:
 This model has six fields. Two foreignkeys, the first one is the "user_id" that's used to assign the user that owns the auction and the "category_id" to assign the category for this auction.

 "Title" field is used to store the title of the auction. 
 
 "Description" is used for the description. 
 
 "Image_url" stores the url for the image that the user provides when creating the auction
 
 "Minimum_bid" stores the minimum price for the first bid

```
class AuctionsListing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=64)

    description = models.CharField(max_length=150)

    image_url = models.CharField(max_length = 400, blank=True, null=True)

    minimum_bid = models.IntegerField()
    is_open = models.BooleanField()
```


### Bids model:
The bids model has just 3 fields. Two of them are foreign keys, the "user_id" for the user that made the bid and the "auction_id" that stores the auction that the user id placing the bid.

The "price" field is the one that stores the price for the bid
```
class Bids(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bid_Owner")
    price = models.IntegerField()
    auction_id = models.ForeignKey(AuctionsListing, on_delete=models.CASCADE)
```

### Watchlist and Comments models:

This two models are very similar so I'm going to show them together.

The watchlist model has just two foreignkey fields "user_id" and "auction_id". The comments model has one more for the coment

```
class watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(AuctionsListing, on_delete=models.CASCADE)


class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comment_Owner")
    auction_id = models.ForeignKey(AuctionsListing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
```