from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Avg
from django.views.decorators.http import require_http_methods

from HelloWorld.Item.templatetags import get_range
from models import Item, BidItem, Rate
# Create your views here.


def list_view(request):
	item_list = Item.objects.all()[:5]
	return render(request, 'ecommerce/grid.html', {'item_list': item_list})


def detail_view(request, pk):
	try:
		item = Item.objects.get(pk=pk)
	except (KeyError, Item.DoesNotExist):
		messages.add_message(request, messages.INFO, "toastr.error('The item you are looking for does not exist', 'Error');")
		return HttpResponseRedirect('/index/')

	rate_num = item.rates.all().aggregate(Avg('num'))['num__avg']
	rates = item.rates.all()
	return render(request, 'ecommerce/detail.html', {'item': item, 'rate_num': rate_num, 'rates': rates})


def add_cart_view(request, pk):
	try:
		item = Item.objects.get(pk=pk)
	except (KeyError, Item.DoesNotExist):
		messages.add_message(request, messages.INFO, "toastr.error('The item you are looking for does not exist', 'Error');")
		return HttpResponseRedirect('/index/')

	request.user.cart.get().items.add(item)
	request.user.cart.get().save()

	messages.add_message(request, messages.INFO, "toastr.success('The item is in your cart now', 'Success');")
	return HttpResponseRedirect('/item/id/'+pk)


