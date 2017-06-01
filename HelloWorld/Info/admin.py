from django.contrib import admin

from models import CreditCard, Address, Order


class CreditCardAdmin(admin.ModelAdmin):
	list_display = ['number', 'expire_date', 'cvv', 'address', 'owner']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['address1', 'address2', 'zip_code', 'state']

class OrderAdmin(admin.ModelAdmin):
	list_display = ('created', 'item', 'buyer', 'status')
	list_filter = ['created']


admin.site.register(Address, AddressAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Order, OrderAdmin)
