"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from .Account import views as auth_view
from .Item import views as item_view

urlpatterns = [
	url(r'^$', item_view.list_view, name='landing'),
	url(r'^index/$', item_view.list_view, name='index'),

	# Auth
	url(r'^login/$', auth_view.login_view, name='login'),
	url(r'^logout/$', auth_view.logout_view, name='logout'),
	url(r'^register/$', auth_view.reg_view, name='reg'),
	url(r'^seller_request/$', auth_view.become_seller_view, name='seller_request'),


	# Items
	url(r'^item/$', item_view.list_view, name='item'),
	url(r'^item/categ/(?P<categ>[0-9]*)/$', auth_view.login_view, name='item_categ'),
	url(r'^item/id/(?P<pk>[0-9]*)/$', item_view.detail_view, name='item_id'),
	url(r'^item/new/n/$', item_view.add_new_item_view, name='item_new'),
	url(r'^item/id/(?P<pk>[0-9]*)/rate/$', item_view.rate_view, name='item_rate'),
	url(r'^checkout/$', item_view.checkout_view, name='checkout'),



	# Cart
	url(r'^item/id/(?P<pk>[0-9]*)/addcart$', item_view.add_cart_view, name='item_add_cart'),
	url(r'^item/id/(?P<pk>[0-9]*)/addbid$', item_view.add_bid_view, name='item_add_bid'),
	url(r'^cart/$', item_view.cart_view, name='item_cart'),
	url(r'^cart/remove/(?P<pk>[0-9]*)$', item_view.remove_cart_view, name='item_remove_cart'),


	# admin
	url(r'^admin/', admin.site.urls),
]
