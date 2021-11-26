import auctions
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.fields import ImageField
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.urls import reverse
from .models import User, Auction, Category, WatchList, Comment
from .forms import Auctionform

def index(request):
    if request.user.is_authenticated:
        current_category = "All"
        auctions = Auction.objects.all()
        if request.POST:
            current_category_id = request.POST.get('dropdown')
            current_category = Category.objects.get(pk=current_category_id).name
            if current_category != "All":
                auctions = Auction.objects.filter(category=current_category_id)

        return render(request, "auctions/index.html", {
            "log_in": True,
            "auctions": auctions,
            "current_category": current_category,
            "Category": Category.objects.all()
        })
    else:
        return render(request, "auctions/index.html", {
            "log_in": False,
            
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
            return HttpResponseRedirect(reverse("auc:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auc:index"))


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
        return HttpResponseRedirect(reverse("auc:index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.user.is_authenticated:
        if request.POST:
            form = Auctionform(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                description = form.cleaned_data["description"]
                bid = form.cleaned_data["start_bid"]
                image = form.cleaned_data["image"]
                category = form.cleaned_data["category"]
                seller = request.user.username

                #add new list to auction
                new_list = Auction(seller=seller, title=title, description=description, start_bid=bid, image=image, category=category)
                new_list.save()

                return HttpResponseRedirect(reverse("auc:index"))
        return render(request, "auctions/create.html", {
            "form":Auctionform()
        })
    return HttpResponseRedirect(reverse("auc:index"))

def list(request, list_id):

    if request.user.is_authenticated:
        list = Auction.objects.get(pk=list_id)
        valid = True
        if request.POST:
            if request.POST['action'] == "Add": #add to watchlist
                WatchList.objects.create(user_id = request.user.id, lists_id = list_id)
            elif request.POST['action'] == "Remove": #remove from watchlist
                dele = WatchList.objects.filter(user_id = request.user.id, lists_id = list_id)
                dele.delete()
                
            elif request.POST['action'] == "Close": #close bid
                list.on_list = False;
                list.save()
            elif request.POST['action'] == "Bid": #place bid
                value = request.POST.get("value")
                #check whether the bid is greater than the starting bid or current bid
                value = int(value)
                if list.current_bid == -1:
                    if value <= list.start_bid:
                        valid = False
                else:
                    if value <= list.current_bid:
                        valid = False
                
                #update the buyer and current_bid
                if valid:
                    list.current_bid = value
                    list.buyer = request.user.username
                    list.save()
            
            elif request.POST["action"] == "Comment": #post comment
                comment = request.POST.get("comment")
                Comment.objects.create(user_id=request.user.id, auction_id=list_id, comment=comment)
                


        #find whether the auction is in the user's WatchList         
        in_watchlist = True
        find_list = WatchList.objects.filter(user_id = request.user.id, lists_id = list_id)
        if len(find_list) == 0:
            in_watchlist = False
        
        #check whether the seller and buyer is the user
        seller = list.seller
        buyer = list.buyer

        if(seller == request.user.username):
            seller = "YOU"
        if(buyer == request.user.username):
            buyer = "YOU"

        #get the comments
        Comments = Comment.objects.filter(auction_id = list_id)

        #markdown the bg of the seller in comment
        seller_name = list.seller
        

        return render(request, "auctions/list_page.html", {
            "list":list,
            "seller": seller,
            "buyer": buyer,
            "in_watchlist": in_watchlist,
            "valid": valid,
            "Comments": Comments,
            "seller_name": seller_name
            
        })
    return HttpResponseRedirect(reverse("auc:index"))

def watchlist(request):
    if request.user.is_authenticated:
        #get the watchlist of the current user
        auctions = WatchList.objects.filter(user = request.user.id)
        return render(request, "auctions/watchlist.html", {
            "auctions": auctions
        })

    return HttpResponseRedirect(reverse("auc:index"))