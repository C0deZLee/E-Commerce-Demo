from __future__ import unicode_literals
from django.db import models

# Create your models here.
from ..Account.models import Account


class Category(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)
	url = models.CharField(max_length=200, null=True, blank=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	phone = models.CharField(max_length=200, null=True, blank=True)

	def __unicode__(self):
		return self.name


class Item(models.Model):
	name = models.CharField(max_length=200)
	listed_price = models.FloatField(null=True, blank=True)
	amount = models.IntegerField()
	description_short = models.CharField(max_length=100, null=True, blank=True)
	description = models.CharField(max_length=1000, null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="items")

	img1 = models.CharField(max_length=200, null=True, blank=True)
	img2 = models.CharField(max_length=200, null=True, blank=True)
	img3 = models.CharField(max_length=200, null=True, blank=True)
	contact = models.CharField(max_length=200, null=True, blank=True)
	year = models.IntegerField(null=True, blank=True)
	new_used = models.CharField(max_length=200, null=True, blank=True)
	make = models.CharField(max_length=200, null=True, blank=True)
	trim = models.CharField(max_length=200, null=True, blank=True)
	mile = models.IntegerField(null=True, blank=True)
	model = models.CharField(max_length=200, null=True, blank=True)
	style = models.CharField(max_length=200, null=True, blank=True)
	engine = models.CharField(max_length=200, null=True, blank=True)
	transmission = models.CharField(max_length=200, null=True, blank=True)
	ex_color = models.CharField(max_length=200, null=True, blank=True)
	in_color = models.CharField(max_length=200, null=True, blank=True)
	vin = models.CharField(max_length=200, null=True, blank=True)
	stock_num = models.CharField(max_length=200, null=True, blank=True)

	def __unicode__(self):
		return self.name


class Rate(models.Model):
	item = models.ForeignKey(Item, related_name='rates')
	content = models.CharField(max_length=200)
	rater = models.ForeignKey(Account)
	num = models.IntegerField()
	created = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.num)


class Order(models.Model):
	created = models.DateTimeField(auto_now=True)
	amount = models.IntegerField(default=0)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	buyer = models.ForeignKey(Account, related_name='purchased')
	seller = models.ForeignKey(Account, related_name='selled')
	# 1: not shipped, 2: shipped, 3: delivered
	status = models.IntegerField(default=1)


