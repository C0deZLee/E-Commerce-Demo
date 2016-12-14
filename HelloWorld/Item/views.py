import json

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Avg, Sum, Q
from django.views.decorators.http import require_http_methods

from forms import BidForm
from models import Item, Rate, Category, Order
from ..Info.models import Cart
# Create your views here.


def list_view(request):
	cate = Category.objects.all()
	item_list = Item.objects.all()[0:9]
	if request.user.is_authenticated:
		if Cart.objects.filter(user=request.user).count() == 0:
			cart = Cart()
			cart.user = request.user
			cart.save()
		else:
			print Cart.objects.filter(user=request.user).count()
	page = 1
	return render(request, 'ecommerce/grid.html', {'item_list': item_list, 'cate': cate, 'page': int(page)})


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


def cate_list_view(request, pk):
	page = 1
	cate = Category.objects.all()
	categ = Category.objects.get(pk=pk)
	item_list = Item.objects.filter(category=categ)[0:9]
	if request.user.is_authenticated:
		if Cart.objects.filter(user=request.user).count() == 0:
			cart = Cart()
			cart.user = request.user
			cart.save()
		else:
			print Cart.objects.filter(user=request.user).count()

	return render(request, 'ecommerce/grid.html', {'item_list': item_list, 'cate': cate, 'page': int(page)})


@require_http_methods(['POST'])
def search_view(request):
	cate = Category.objects.all()

	item_list = Item.objects.all()
	if request.POST['price-min']:
		item_list = item_list.filter(listed_price__gte=request.POST['price-min'])
	if request.POST['price-max']:
		item_list = item_list.filter(listed_price__lte=request.POST['price-max'])
	if request.POST['year-min']:
		item_list = item_list.filter(year__gte=request.POST['year-min'])
	if request.POST['year-max']:
		item_list = item_list.filter(year__lte=request.POST['year-max'])
	if request.POST['mile-min']:
		item_list = item_list.filter(mile__gte=request.POST['mile-min'])
	if request.POST['mile-max']:
		item_list = item_list.filter(mile__lte=request.POST['mile-max'])
	if request.POST['brand']:
		item_list = item_list.filter(name__contains=request.POST['brand'])

	try:
		if request.POST['nu'] == "n":
			item_list = item_list.filter(new_used="New")
		elif request.POST['nu'] == "u":
			item_list = item_list.filter(new_used="Used")
	except:
		pass

	try:
		if request.POST['mile'] == "high":
			item_list = item_list.order_by('-mile')
		else:
			item_list = item_list.order_by('mile')
	except:
		pass


	try:
		if request.POST['year'] == "high":
			item_list = item_list.order_by('-year')
		else:
			item_list = item_list.order_by('year')
	except:
		pass

	try:
		if request.POST['price'] == "high":
			item_list = item_list.order_by('-listed_price')
		else:
			item_list = item_list.order_by('listed_price')
	except:
		pass

	return render(request, 'ecommerce/grid.html', {'item_list': item_list, 'cate': cate, 'page': False, })



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

	request.user.cart.get().items.add(item)
	request.user.cart.get().save()

	messages.add_message(request, messages.INFO, "toastr.success('The item is in your watchlist now', 'Success');")
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
	cate = Category.objects.all()
	cart_items = request.user.cart.get().items.all()
	total = request.user.cart.get().items.aggregate(Sum('listed_price'))['listed_price__sum']

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
				request.user.cart.get().items.remove(item)
				request.user.cart.get().save()
				order = Order()
				order.item = item
				order.amount = 1
				order.seller = order.item.provider
				order.buyer = request.user
				order.status = 1
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
		if order.status != 3:
			order.status += 1
			order.save()
	else:
		messages.add_message(request, messages.INFO, "toastr.error('The record you are looking for does not exist', 'Error');")

	return HttpResponseRedirect('/sells/')


def import_data_view(request):
	f = open("car.json", "r")
	counter = 1
	for line in f:
		try:
			j_item = json.loads(line)
			item = Item()
			item.contact = j_item["Contact"]
			item.amount = 1
			item.description_short = j_item["Description"][0:50]
			item.engine = j_item["Engine"]
			item.ex_color = j_item["ExColor"]
			item.img1 = j_item["ImgURL1"]
			item.img2 = j_item["ImgURL2"]
			item.img3 = j_item["ImgURL3"]
			item.in_color = j_item["InColor"]
			item.make = j_item["Make"]
			item.style = j_item["Style"]
			item.mile = int(j_item["Mile"])
			item.vin = j_item["VIN"]
			item.new_used = j_item["New_Used"]
			if j_item["Price"] == "":
				item.listed_price = 0
			else:
				item.listed_price = int(j_item["Price"])
			item.transmission = j_item["Transmission"]
			item.model = j_item["Model"]
			item.trim = j_item["Trim"]
			item.year = int(j_item["Year"])
			item.name = j_item["CarName"]
			item.stock_num = j_item["StockNum"]

			if "Workman" in j_item["DealerName"]:
				item.category = Category.objects.get(pk=8)

			if "Bobby Rahal Toyota" in j_item["DealerName"]:
				item.category = Category.objects.get(pk=9)

			if "Sutliff Buick GMC" in j_item["DealerName"]:
				item.category = Category.objects.get(pk=10)

			if "Bobby Rahal Honda" in j_item["DealerName"]:
				item.category = Category.objects.get(pk=11)

			if "StateCollegeMotors" in j_item["DealerName"]:
				item.category = Category.objects.get(pk=12)

			if "Chevrolet" in j_item["DealerName"]:
				item.category = Category.objects.get(pk=13)

			if "Ford" in j_item["DealerName"]:
				item.category = Category.objects.get(pk=14)

			if "Mitsubishi" in j_item["DealerName"]:
				item.category = Category.objects.get(pk=15)

			if "Lexus" in j_item["DealerName"]:
				item.category = Category.objects.get(pk=16)

			item.save()
			counter = counter + 1
		except:
			print counter
	return HttpResponse("Success")
