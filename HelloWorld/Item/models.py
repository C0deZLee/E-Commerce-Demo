from __future__ import unicode_literals
from django.db import models

# Create your models here.
from ..Account.models import Account


class Category(models.Model):
	level = models.IntegerField()
	name = models.CharField(max_length=200)
	parentID = models.ForeignKey('self', null=True, blank=True)

	def __unicode__(self):
		return self.name


class BidItem(models.Model):
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	reserved_price = models.FloatField()
	action_price = models.FloatField(null=True, blank=True)
	current_price = models.FloatField()

	def __unicode__(self):
		return str(self.end_time)

	@property
	def _name(self):
		return self.end_time


class Item(models.Model):
	name = models.CharField(max_length=200)
	keywords = models.CharField(max_length=200)
	provider = models.ForeignKey(Account, on_delete=models.CASCADE)
	listed_price = models.FloatField(null=True, blank=True)
	amount = models.IntegerField()
	description_short = models.CharField(max_length=100, null=True, blank=True)
	description = models.CharField(max_length=1000, null=True, blank=True)
	bid = models.ForeignKey(BidItem, on_delete=models.CASCADE, null=True, blank=True, related_name="item", unique=True)
	category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="items")

	def __unicode__(self):
		return self.name

	@property
	def _type(self):
		if self.listed_price:
			return 'Sale Item'
		else:
			return 'Bid Item'


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


