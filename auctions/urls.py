from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("auctions/<int:auction_id>", views.auction, name="auction"),
    path("watchlist/watch/<int:user_id>/<int:auction_id>", views.watch, name="watch"),
    path("watchlist/unwatch/<int:user_id>/<int:auction_id>", views.unwatch, name="unwatch"),
    path("bid/placebid/<int:user_id>/<int:auction_id>", views.placebid, name="placebid"),
    path("auctions/close/<int:user_id>/<int:auction_id>", views.close, name="close"),
    path("auctions/comments/add/<int:user_id>/<int:auction_id>", views.comment, name="comment"),
    path("watchlist/<int:user_id>", views.user_watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("closed", views.closed, name="closed")
]
