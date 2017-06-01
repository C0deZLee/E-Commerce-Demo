from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from forms import UserChangeForm, UserCreationForm
from models import Account, AccountDetail, Cart
# Register your models here.

class AccountAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'is_admin')
    list_filter = ['is_admin']
    readonly_fields = ('created', 'updated')
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
         ),
    )
    fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('email', 'username',),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()

class AccountDetailAdmin(admin.ModelAdmin):
    list_display = ['user', 'address']

class CartAdmin(admin.ModelAdmin):
        fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('user', 'items',),
        }),
    )


admin.site.register(Cart, CartAdmin)
admin.site.register(AccountDetail, AccountDetailAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)
