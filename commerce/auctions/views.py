from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .forms import CreateListingForm, CommentForm
from django.contrib import messages
from .models import User, AuctionListing, Categories, WatchList, Comments, Bids
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from time import gmtime, strftime


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


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
        return redirect("index")
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.seller = request.user
            instance.current_price = instance.starting_bid
            instance.save()
            if instance is not None:
                messages.success(request, "New listing created for {}".format(instance))
                return redirect("index")
            else:
                messages.warning(request, "No listing created.")

    else:
        form=CreateListingForm()
    return render(request, "auctions/createlisting.html", {"form": form})


def active_listings(request):
    active = AuctionListing.active.all()
    return render(request, "auctions/index.html", {"listings": active})


def closed_listings(request):
    # show only listings that have been sold
    sold = AuctionListing.objects.filter(status="Sold")
    return render(request, "auctions/closedlistings.html", {"listings": sold})


class ListingDetailView(DetailView):
    model = AuctionListing
    template_name = "auctions/detiallisting.html"
    context_object_name = "listing"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # get all the contents for this detailed view object
        comments_connected = Comments.objects.filter(listing=self.get_object())
        # pass data to the template for rendering
        data['comments'] = comments_connected
        data["comment_form"] = CommentForm()

        instance = get_object_or_404(AuctionListing, pk=self.object.pk)
        if self.request.user.is_authenticated:
            liked = False
            if instance.likes.filter(id=self.request.user.id):
                liked = True
            data['liked'] = liked
            data['liked_by'] = instance.likes.all()

            watched = False
            if WatchList.objects.filter(items=instance, user=self.request.user).exists():
                watched = True
            data["watched"] = watched

            # checks if bidding is closed and user won that bid, then display winning message
            if instance.bidding_open is False:
                if Bids.objects.filter(listing=instance, buyer=self.request.user):
                    messages.success(self.request, "Congratulations, You have won this bid")
            else:
                # if auction is still open, checks if user is in the lead for bids
                if Bids.objects.filter(buyer=self.request.user, amount=instance.current_price).exists():
                    messages.info(self.request, "You are in the lead in this auction!")

        return data

    def post(self, request, *args, **kwargs):
        # create an instance of Comments using the data passed from the post request
        new_comment = Comments(content=request.POST.get('content'),
                               author=self.request.user,
                               listing=self.get_object())
        new_comment.save()
        return redirect("item", self.get_object())
        # return self.get(self, request, *args, **kwargs)


def categories(request):
    category = Categories.objects.all()
    return render(request, "auctions/categories.html", {"categories": category})


def category_listing(request, title):
    listings = AuctionListing.objects.filter(category__title=title)
    return render(request, "auctions/categorylistings.html", {"listings": listings, "category": title})


@login_required
def add_remove_watchlist(request, id):
    watchlist = WatchList.objects.get(user=request.user)
    item = get_object_or_404(AuctionListing, pk=id)
    if WatchList.objects.filter(user=request.user, items=item).exists():
        watchlist.items.remove(item)
        return redirect('item', item.slug)
    else:
        user_list, created = WatchList.objects.get_or_create(user=request.user)
        user_list.items.add(item)
    return redirect('item', item.slug)


@login_required
def my_watchlist(request):
    try:
        watchlist = WatchList.objects.get(user=request.user)
        items = watchlist.items.all()
        number = items.count()
    except:
        watchlist = None

    return render(request, 'auctions/watchlist.html', {"listings": items, "number": number})


@login_required
def liked_items(request):
    likelist = request.user.listing_likes.all()
    return render(request, 'auctions/likelist.html', {'listings': likelist})


@login_required
def my_listings(request):
    mylistings = AuctionListing.objects.filter(seller=request.user)
    return render(request, 'auctions/mylistings.html', {'listings': mylistings})


@login_required
def add_remove_likes(request, id):
    item = get_object_or_404(AuctionListing, id=id)
    if item.likes.filter(id=request.user.id).exists():
        item.likes.remove(request.user)
    else:
        item.likes.add(request.user)
    return redirect('item', item.slug)


@login_required
def bid(request, id):
    listing = AuctionListing.objects.get(id=id)
    if request.method == "POST":
        bid_amount = float(request.POST["bid_amount"])
        # automatically add to watchlist once user makes a bid for an item
        user_list, created = WatchList.objects.get_or_create(user=request.user)
        user_list.items.add(listing)
        current_bids = Bids.objects.filter(listing=listing)
        # check if bid amount is more than the starting price
        if bid_amount < listing.starting_bid:
            messages.warning(request, "Please make a higher bid than the starting price {}".format(listing.starting_bid))
            return redirect('item', listing.slug)
        # check if bid amount is more than the most current price
        elif bid_amount < listing.current_price or current_bids.filter(amount__gte = bid_amount):
            messages.warning(request, "Please make a higher bid than the current price {}".format(listing.current_price))
            return redirect('item', listing.slug)
        else:
            listing.current_price = bid_amount
            listing.save()
            bidder = User.objects.get(id=int(request.user.id))
            date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            Bids.objects.create(buyer=bidder, date=date, amount=bid_amount, listing=listing)
            messages.success(request, "You have made successfully made a bid of ${}. Good Luck!".format(listing.current_price))
    return redirect("item", listing.slug)


@login_required
def close_bid(request, id):
    listing = AuctionListing.objects.get(id=id)
    if request.method == "POST":
        listing.bidding_open = False
        try:
            winning_bid = Bids.objects.filter(listing=listing).order_by('-amount').first()
            messages.success(request, "Congratulations! You have sold {} to {} for ${}"
                             .format(listing, winning_bid.buyer, winning_bid.amount))
            listing.status = "Sold"
            listing.winner = winning_bid.buyer
        except:
            messages.info(request, "No bids received.")
            listing.status = "Closed"
    listing.save()
    return redirect("item", listing.slug)


@login_required
def bids_won(request):
    # items_won = AuctionListing.closed.filter(bids__buyer=request.user).distinct()
    items_won = AuctionListing.closed.filter(winner=request.user)
    return render(request, "auctions/bidswon.html", {"listings": items_won})

