from django.urls import path

from . import views

urlpatterns = [
    path("home", views.active_listings, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("auction/create/", views.create_listing, name="create"),
    path("listings/<slug:slug>", views.ListingDetailView.as_view(), name="item"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:title>", views.category_listing, name="categories-listings"),
    # path("watchlist/add/<int:id>", views.add_to_watchlist, name="watchlist-add"),
    # path("watchlist/remove/<int:id>", views.remove_from_watchlist, name="watchlist-remove"),
    path("watchlist/<int:id>", views.add_remove_watchlist, name="watch"),
    path("mywatchlist/", views.my_watchlist, name="mywatchlist"),
    path("like/<int:id>", views.add_remove_likes, name="like"),
    path("likelist/", views.liked_items, name="likelist"),
    path("mylistings/", views.my_listings, name="mylistings"),
    path("closedlistings/", views.closed_listings, name="closedlistings"),
    path("closebid/<int:id>", views.close_bid, name="close"),
    path("makebid/<int:id>", views.bid, name="bid"),
    path("bidswon/", views.bids_won, name="won")
]
