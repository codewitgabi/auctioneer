from django.contrib import admin
from .models import Lot, Bid, LotImage


class LotImageInline(admin.TabularInline):
	model = LotImage


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "increment", "auction_date")
	list_filter = ("auction_date", "price")
	search_fields = ("name",)
	inlines = (LotImageInline,)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
	list_display = ("bidder", "bid")

