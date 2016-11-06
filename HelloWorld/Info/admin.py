from django.contrib import admin

from models import CreditCard
# Register your models here.


class CreditCardAdmin(admin.ModelAdmin):
	list_display = ['number', 'expire_date', 'cvv', 'address', 'owner']

admin.site.register(CreditCard, CreditCardAdmin)