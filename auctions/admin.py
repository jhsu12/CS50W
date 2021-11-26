from django.contrib import admin
from .models import Auction, User, Category, WatchList, Comment

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "seller","date_posted", "title", "description", "start_bid", "image", "category", "current_bid", "buyer", "on_list")
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

admin.site.register(Auction, AuctionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(WatchList)
admin.site.register(Comment)