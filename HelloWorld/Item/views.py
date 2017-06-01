import json

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Avg, Sum, Q
from django.views.decorators.http import require_http_methods

from forms import BidForm
from models import Item, Rate, Category
from ..Info.models import Order
from ..Account.models import Cart

# Create your views here.


def list_view(request):
	item_list = Item.objects.all()[:9]
	return render(request, 'ecommerce/grid.html', {'item_list': item_list, 'title': 'Today'})


def page_list_view(request, page):
	cate = Category.objects.all()
	item_list = Item.objects.all()[0+int(page)*9:9+int(page)*9]
	if request.user.is_authenticated:
		if Cart.objects.filter(user=request.user).count() == 0:
			cart = Cart()
			cart.user = request.user
			cart.save()
		else:
			print Cart.objects.filter(user=request.user).count()

	return render(request, 'ecommerce/grid.html', {'item_list': item_list, 'cate': cate, 'page': int(page)})



def detail_view(request, pk):
	cate = Category.objects.all()

	try:
		item = Item.objects.get(pk=pk)
	except (KeyError, Item.DoesNotExist):
		messages.add_message(request, messages.INFO, "toastr.error('The item you are looking for does not exist', 'Error');")
		return HttpResponseRedirect('/index/')

	rate_num = item.rates.all().aggregate(Avg('num'))['num__avg']
	rates = item.rates.all()
	return render(request, 'ecommerce/detail.html', {'item': item, 'rate_num': rate_num, 'rates': rates, 'cate' : cate})



def add_cart_view(request, pk):
	try:
		item = Item.objects.get(pk=pk)
	except (KeyError, Item.DoesNotExist):
		messages.add_message(request, messages.INFO, "toastr.error('The item you are looking for does not exist', 'Error');")
		return HttpResponseRedirect('/index/')

	if item.provider == request.user:
		messages.add_message(request, messages.INFO, "toastr.error('You cannot buy your own item!', 'Error');")
		return HttpResponseRedirect('/item/id/'+pk)

	request.user.cart.items.add(item)
	request.user.cart.save()

	messages.add_message(request, messages.INFO, "toastr.success('The item is in your watchlist now', 'Success');")
	return HttpResponseRedirect('/item/id/'+pk)


def remove_cart_view(request, pk):
	try:
		item = Item.objects.get(pk=pk)
	except (KeyError, Item.DoesNotExist):
		messages.add_message(request, messages.INFO, "toastr.error('The item you are looking for does not exist', 'Error');")
		return HttpResponseRedirect('/index/')

	request.user.cart.items.remove(item)
	request.user.cart.save()

	messages.add_message(request, messages.INFO, "toastr.success('The item is removed from your cart.', 'Success');")
	return HttpResponseRedirect('/cart/')


def cart_view(request):
	cart_items = request.user.cart.items.filter(type=0)
	total = request.user.cart.items.filter(type=0).aggregate(Sum('listed_price'))['listed_price__sum']

	bid_items = request.user.cart.items.filter(type=1)

	if total is None:
		total = 0
	return render(request, 'ecommerce/cart.html', {'cart_items': cart_items, 'total': total, 'cate' : cate})


def add_new_item_view(request):
	if request.user.is_seller is False:
		messages.add_message(request, messages.INFO, "toastr.error('You must be a seller to post items', 'Error');")
		return HttpResponseRedirect('/index')

	if request.method == 'POST':
		item = Item()
		try:
			item.description = request.POST['desl']
		except:
			pass
		try:
			item.keywords = request.POST['key']
		except:
			pass
		item.amount = request.POST['amount']
		item.name = request.POST['name']
		item.category = Category.objects.get(pk=request.POST['cate'])
		item.description_short = request.POST['dess']
		item.provider = request.user
		item.listed_price = request.POST['price']

		try:
			item.save()
		except:
			messages.add_message(request, messages.INFO, "toastr.error('You provided wrong data.', 'Error');")

	return render(request, 'ecommerce/newitem.html')


@require_http_methods(['POST'])
def rate_view(request, pk):
	try:
		item = Item.objects.get(pk=pk)
	except (KeyError, Item.DoesNotExist):
		messages.add_message(request, messages.INFO, "toastr.error('The item you are looking for does not exist', 'Error');")
		return HttpResponseRedirect('/index/')
	#
	# if item.provider == request.user:
	# 	messages.add_message(request, messages.INFO, "toastr.error('You cannot buy your own item!', 'Error');")
	# 	return HttpResponseRedirect('/item/id/'+pk)

	rate = Rate()
	rate.item = item
	rate.num = request.POST['num']
	rate.rater = request.user
	rate.content = request.POST['content']

	rate.save()

	messages.add_message(request, messages.INFO, "toastr.success('You have left a comment.', 'Success');")
	return HttpResponseRedirect('/item/id/'+pk)


def checkout_view(request):
	cart_items = request.user.cart.get().items
	total = request.user.cart.get().items.aggregate(Sum('listed_price'))['listed_price__sum']

	if request.method == 'POST':
		if cart_items.count == 0:
			messages.add_message(request, messages.INFO, "toastr.success('Your cart is empty.', 'Error');")
			return HttpResponseRedirect('/index/')

		else:
			for item in cart_items:
				item.amount -= 1
				request.user.cart.items.remove(item)
				request.user.cart.save()
				order = Order(item = item, amount = 1, seller = order.item.provider, buyer = request.user, status = 0)
				order.save()
			messages.add_message(request, messages.INFO, "toastr.success('Purchase completed.', 'Success');")
			return HttpResponseRedirect('/history/')

	return render(request, 'ecommerce/payment.html', {'cart_items': cart_items, 'total': total})


def order_history_view(request):
	history = Order.objects.filter(buyer=request.user)
	return render(request, 'ecommerce/order-history.html', {'history': history})


def sell_history_view(request):
	if not request.user.is_seller:
		messages.add_message(request, messages.INFO, "toastr.error('You are not seller', 'Error');")
		return HttpResponseRedirect('/index/')
	history = Order.objects.filter(seller=request.user)
	return render(request, 'ecommerce/sell-history.html', {'history': history})


def change_order_status_view(request, pk):
	try:
		order = Order.objects.get(pk=pk)
	except (KeyError, Order.DoesNotExist):
		messages.add_message(request, messages.INFO, "toastr.error('The record you are looking for does not exist', 'Error');")
		return HttpResponseRedirect('/index/')

	if order.seller == request.user:
		if order.status < 3:
			order.status += 1
			order.save()
	else:
		messages.add_message(request, messages.INFO, "toastr.error('The record you are looking for does not exist', 'Error');")

	return HttpResponseRedirect('/sells/')
