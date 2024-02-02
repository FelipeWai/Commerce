from django.contrib import admin
from .models import User, AuctionsListing, Categories, watchlist, Bids, Comments

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class AuctionsAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "category_id", "title")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "auction_id")

class BidsAdmin(admin.ModelAdmin):
    list_display = ("user_id", "price", "auction_id")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("user_id", "auction_id", "comment")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(AuctionsListing, AuctionsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(watchlist, WatchlistAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments)