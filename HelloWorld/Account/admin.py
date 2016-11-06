from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from forms import UserChangeForm, UserCreationForm
from models import Account, Address, Seller


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
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()


class AddressAdmin(admin.ModelAdmin):
    list_display = ['address1', 'address2', 'zip_code', 'state']


class SellerAdmin(admin.ModelAdmin):
    list_display = ['is_enterprise', 'account']

admin.site.register(Address, AddressAdmin)
admin.site.register(Account, AccountAdmin)
# ... and, since we're not using Django's built-in permissions, unregister the Group model from admin.
admin.site.unregister(Group)
