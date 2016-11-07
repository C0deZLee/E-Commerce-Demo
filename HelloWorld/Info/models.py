from __future__ import unicode_literals

from django.db import models
# Create your models here.
from ..Account.models import Address, Account
from ..Item.models import Item


class Cart(models.Model):
	user = models.ForeignKey(Account, related_name='cart', unique=True)
	items = models.ManyToManyField(Item, blank=True, null=True)
