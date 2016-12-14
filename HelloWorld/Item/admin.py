from django.contrib import admin

from models import Item, Rate, Category, Order
# Register your models here.


class ItemAdmin(admin.ModelAdmin):
	list_display = ['name', 'category', 'listed_price']


class RateAdmin(admin.ModelAdmin):
	list_display = ['item', 'rater', 'num', 'created']


class CategoryAdmin(admin.ModelAdmin):
	list_display = ['pk', 'name']


class OrderAdmin(admin.ModelAdmin):
	list_display = ('created', 'item', 'buyer', 'status')
	list_filter = ['created']


admin.site.register(Item, ItemAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
