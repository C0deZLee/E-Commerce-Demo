from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Avg, Sum, Q
from django.views.decorators.http import require_http_methods

from forms import BidForm
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


def remove_cart_view(request, pk):
	try:
		item = Item.objects.get(pk=pk)
	except (KeyError, Item.DoesNotExist):
		messages.add_message(request, messages.INFO, "toastr.error('The item you are looking for does not exist', 'Error');")
		return HttpResponseRedirect('/index/')

	request.user.cart.get().items.remove(item)
	request.user.cart.get().save()

	messages.add_message(request, messages.INFO, "toastr.success('The item is removed from your cart.', 'Success');")
	return HttpResponseRedirect('/cart/')


def cart_view(request):
	cart_items = request.user.cart.get().items.filter(bid=None)
	total = request.user.cart.get().items.filter(bid=None).aggregate(Sum('listed_price'))['listed_price__sum']

	bid_items = request.user.cart.get().items.filter(~Q(bid=None))

	if total is None:
		total = 0
	return render(request, 'ecommerce/cart.html', {'cart_items': cart_items, 'total': total, 'bid_items': bid_items})


@require_http_methods(['POST'])
def add_bid_view(request, pk):
	try:
		item = Item.objects.get(pk=pk)
	except (KeyError, Item.DoesNotExist):
		messages.add_message(request, messages.INFO, "toastr.error('The item you are looking for does not exist', 'Error');")
		return HttpResponseRedirect('/index/')

	if request.POST['newbid']:
		newbid = request.POST['newbid']
		item.bid.current_price = newbid
		item.bid.save()
		request.user.cart.get().items.add(item)
		request.user.cart.get().save()



		messages.add_message(request, messages.INFO, "toastr.success('The item is in your cart now', 'Success');")
		return HttpResponseRedirect('/item/id/'+pk)
	else:
		messages.add_message(request, messages.INFO, "toastr.error('Wrong price.', 'Error');")
		return HttpResponseRedirect('/item/id/'+pk)