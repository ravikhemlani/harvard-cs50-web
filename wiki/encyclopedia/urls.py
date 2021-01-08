from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.render_page, name="entry"),
    path("create/", views.create_page, name="create"),
    path("random/", views.random_page, name="random"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit"),
    path("wiki/search", views.search_results, name="search"),
]
