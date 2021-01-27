from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AuctionListing, User, Bids, Categories, Comments, WatchList

# Register your models here.
admin.site.site_header = "Auctions Administrator"
admin.site.site_title = "Auctions Admin"
admin.site.index_title = "Auctions Site Administration"
admin.site.site_url = None

admin.site.register(User, UserAdmin)
admin.site.register(Categories)
admin.site.register(Bids)
admin.site.register(WatchList)


@admin.register(AuctionListing)
class AuctionAdmin(admin.ModelAdmin):
    readonly_fields = ["slug", "winner", "likes"]
    list_display = ["title", 'category', 'starting_bid', 'uploaded', 'seller', 'status']


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["listing"]

# class UserAdmin(admin.ModelAdmin):
#     list_display = ["email"]
