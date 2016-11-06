from __future__ import unicode_literals
from django.db import models

# Create your models here.
from ..Account.models import Account


class Item(models.Model):
	name = models.CharField(max_length=200)
	keywords = models.CharField(max_length=200)
	provider = models.ForeignKey(Account, on_delete=models.CASCADE)
	listed_price = models.IntegerField()
	# rates


class BidItem(models.Model):
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	reserved_price = models.IntegerField()
	action_price = models.IntegerField(null=True, blank=True)
	item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True, related_name="bid", unique=True)


class Rate(models.Model):
	item = models.ForeignKey(Item, related_name='rates')
	rater = models.ForeignKey(Account)
	num = models.IntegerField()
	created = models.DateTimeField(auto_created=True)


class Category(models.Model):
	level = models.IntegerField()
	name = models.CharField(max_length=200)
	childID = models.ForeignKey('self', related_name='parentID', null=True)
	# parentID = models.ForeignKey('self', related_name='')


class Order(models.Model):
	created = models.DateTimeField(auto_created=True)
	amount = models.IntegerField(default=0)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	buyer = models.ForeignKey(Account, related_name='purchased')
	# 0: not shipped 1: shipped 2: delivered
	status = models.IntegerField(default=0)
