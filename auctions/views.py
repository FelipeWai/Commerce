from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, AuctionsListing, Comments, Categories, Bids, watchlist
from django.contrib.auth.decorators import login_required
from .forms import CreateListingForm
from django.db.models import Max
from django.contrib import messages


from .models import User


def index(request):
    # GET THE AUCTIONS WITHS ITS CURRENT BID
    auctions = AuctionsListing.objects.annotate(
        current_bid=Max('bids__price')
    ).all()

    # RENDER THE PAGE NORMALLY
    return render(request, "auctions/index.html", {
        "auctions": auctions,
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


# CREATE LISTING VIEW
@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            # GET THE USER THATS CREATING THE LISTING
            user = request.user

            # GETTING THE INFORMATION FROM THE LISTING
            category_name = form.cleaned_data['category']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image_url = form.cleaned_data['image_url']
            starting_bid = form.cleaned_data['starting_bid']
            # THE AUCTION WILL ALWAYS START AS OPEN
            is_open = True

            # IF THERES A CATEGORY
            if category_name:
                # QUERY TO GET THE CATEGORY OBJECT
                category_instance = Categories.objects.get(id=category_name)
                new_listing = AuctionsListing(
                    user_id=user,
                    # ASSIGN THE CATEGORY OBJECT TO THE FIELD AT AUCTIONS TABLE
                    category_id=category_instance,
                    title=title,
                    description=description,
                    image_url=image_url,
                    minimum_bid=starting_bid,
                    is_open=is_open
                )
            else:
                new_listing = AuctionsListing(
                    user_id=user,
                    title=title,
                    description=description,
                    image_url=image_url,
                    minimum_bid=starting_bid,
                    is_open=is_open
                )

            # SAVE THE AUCTION AT THE DB
            try:
                new_listing.save()
                return HttpResponseRedirect(reverse("index"))
            except Exception as e:
                message = e
                return render(request, "auctions/create.html", {
                    "form": form,
                    "message": message
                })

    # IF THE METHOD IS GET JUST RENDER THE PAGE NORMALLY
    form = CreateListingForm()
    return render(request, "auctions/create.html", {
        "form": form
        })


def auction(request, auction_id):
    auction = AuctionsListing.objects.get(id=auction_id)

    # GET THE MAXIMUM BID
    max_bid = Bids.objects.filter(auction_id=auction).order_by('-price').first()
    
    # QUERY FOR THE USER WATCHLIST
    user = request.user
    try:
        watchlist_query = watchlist.objects.get(user_id=user.id, auction_id=auction_id)
        is_watched = True
    except:
        is_watched = False

    # QUERY FOR THE COMMENTS
    comments = Comments.objects.filter(auction_id=auction_id)

    return render(request, "auctions/auction.html", {
        "auction": auction,
        "bid": max_bid,
        "is_watched": is_watched,
        "comments": comments
    })

@login_required(login_url='/login')
def watch(request, user_id, auction_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        auction = AuctionsListing.objects.get(id=auction_id)
        watch = watchlist.objects.create(user_id=user, auction_id=auction)
        return HttpResponseRedirect(reverse("auction", args=[auction_id]))
    return HttpResponseNotAllowed(permitted_methods=['POST'])

@login_required(login_url='/login')
def unwatch(request, user_id, auction_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        auction = AuctionsListing.objects.get(id=auction_id)
        watch = watchlist.objects.get(user_id=user, auction_id=auction).delete()
        return HttpResponseRedirect(reverse("auction", args=[auction_id]))
    return HttpResponseNotAllowed(permitted_methods=['POST'])

@login_required(login_url='/login')
def placebid(request, user_id, auction_id):
    if request.method == "POST":
        #GET THE AUCTION, THE USER AND THE MAXIMUM BID FOR THE AUCTION
        auction = AuctionsListing.objects.get(id=auction_id)
        
        # USER OBJ FOR BIDS TABLE
        user_obj = User.objects.get(id=user_id)

        # MAKE SURE THE USER IS THE RIGHT ONE
        is_user = request.user

        #GETTING THE MAXIMUM BID
        max_bid_obj = Bids.objects.filter(auction_id=auction).order_by('-price').first()

        # GETTING THE PRICE FROM THE FORM
        try:
            int_new_bid = new_bid = int(request.POST["price"])
        except:
            messages.error(request, "The bid needs to be a number!")
            return HttpResponseRedirect(reverse("auction", args=[auction_id]))

        # When I tested I dint needed this lines but its more protection i think
        if is_user.id != user_id:
            return HttpResponseBadRequest()
        elif is_user.id == auction.user_id.id:
            return HttpResponse("YOU CAN'T DO IT, U OWN THE AUCTION")

        if not max_bid_obj:
            if int_new_bid < auction.minimum_bid:
                messages.error(request, "Your bid must be equal to or higher than the minimum bid.")
                return HttpResponseRedirect(reverse("auction", args=[auction_id]))
            else:
                bid = Bids(
                    user_id=user_obj,
                    auction_id=auction,
                    price=int_new_bid
                )
                try:
                    bid.save()
                    return HttpResponseRedirect(reverse("auction", args=[auction_id]))
                except:
                    HttpResponse("AQUI")
        else:
            if is_user.id == max_bid_obj.user_id.id:
                messages.error(request, "You already own the bid!")
                return HttpResponseRedirect(reverse("auction", args=[auction_id]))
            
            if int_new_bid <= max_bid_obj.price:
                messages.error(request, "Your bid must be higher than the actual bid.")
                return HttpResponseRedirect(reverse("auction", args=[auction_id]))
            else:
                bid = Bids(
                    user_id=user_obj,
                    auction_id=auction,
                    price=int_new_bid
                )
                try:
                    bid.save()
                    return HttpResponseRedirect(reverse("auction", args=[auction_id]))
                except:
                    HttpResponse("AQUI")
                

    return HttpResponseNotAllowed(permitted_methods=['POST'])


@login_required(login_url='/login')
def close(request, user_id, auction_id):
    if request.method == "POST":
        # MAKE SURE THE USER IS THE RIGHT ONE
        is_user = request.user
        
        auction = AuctionsListing.objects.get(id=auction_id)

        if is_user.id != user_id:
            return HttpResponse("NOT ALLOWED")
        
        if not auction.is_open:
            messages.error(request, "The auction is already closed")
            return HttpResponseRedirect(reverse("auction", args=[auction_id]))

        auction.is_open = False
        auction.save()
        messages.success(request, "Auction closed successfully")
        return HttpResponseRedirect(reverse("auction", args=[auction_id]))

    return HttpResponseNotAllowed(permitted_methods=['POST'])

@login_required(login_url='/login')
def comment(request, user_id, auction_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        auction = AuctionsListing.objects.get(id=auction_id)
        comment = request.POST["comment"]

        new_comment = Comments(
            user_id=user,
            auction_id=auction,
            comment=comment
        )

        new_comment.save()
        return HttpResponseRedirect(reverse("auction", args=[auction_id]))


    return HttpResponseNotAllowed(permitted_methods=['POST'])

@login_required(login_url='/login')
def user_watchlist(request, user_id):
    user = User.objects.get(id=user_id)
    user_watchlist = watchlist.objects.filter(user_id=user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": user_watchlist
    })

def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_id):
    category = Categories.objects.get(id=category_id)
    auctions = AuctionsListing.objects.filter(category_id=category)
    return render(request, "auctions/category.html", {
        "auctions": auctions,
        "category": category
    })

def closed(request):
    # GET THE AUCTIONS WITHS ITS CURRENT BID
    auctions = AuctionsListing.objects.annotate(
        current_bid=Max('bids__price')
    ).all()

    # RENDER THE PAGE NORMALLY
    return render(request, "auctions/closed.html", {
        "auctions": auctions,
    })