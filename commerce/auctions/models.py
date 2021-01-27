from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class User(AbstractUser):
    pass


class ActiveListings(models.Manager):
    def get_queryset(self):
        return super(ActiveListings, self).get_queryset().filter(bidding_open="True")


class ClosedListings(models.Manager):
    def get_queryset(self):
        return super(ClosedListings, self).get_queryset().filter(bidding_open="False")


class Categories(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class AuctionListing(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=50, unique=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="winner")
    description = models.TextField(max_length=500)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)
    current_price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ForeignKey(Categories, null=True, on_delete=models.SET_NULL)
    image = models.URLField(max_length=100, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="listing_likes")
    bidding_open = models.BooleanField(default=True)
    status = models.CharField(max_length=10, default="Active")

    objects = models.Manager()
    active = ActiveListings()
    closed = ClosedListings()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-uploaded"]
        verbose_name_plural = "Auction Listings"

    @property
    def number_of_likes(self):
        return self.likes.count()

    @property
    def number_of_comments(self):
        return Comments.objects.filter(listing=self).count()

    @property
    def num_of_bids(self):
        return Bids.objects.filter(listing=self).count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Bids(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="bids")
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Bids"

    def __str__(self):
        return f'{self.listing} - ${self.amount}'


class Comments(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name_plural = "Comments"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None)
    items = models.ManyToManyField(AuctionListing, related_name="watchlist_items")

    def __str__(self):
        return f"{self.user}'s Watchlist"













