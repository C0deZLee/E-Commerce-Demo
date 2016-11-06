from django.contrib import admin

from models import Item, BidItem, Rate, Category, Order
# Register your models here.


class ItemAdmin(admin.ModelAdmin):
	list_display = ['name', 'keywords', 'bid', 'listed_price']


class BidItemAdmin(admin.ModelAdmin):
	list_display = ['start_time', 'end_time', 'reserved_price', 'action_price']


class RateAdmin(admin.ModelAdmin):
	list_display = ['item', 'rater', 'num', 'created']


class CategoryAdmin(admin.ModelAdmin):
	list_display = ['level', 'name']


class OrderAdmin(admin.ModelAdmin):
	list_display = ('created', 'item', 'buyer')
	list_filter = ['created']


admin.site.register(Item, ItemAdmin)
admin.site.register(BidItem, BidItemAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
