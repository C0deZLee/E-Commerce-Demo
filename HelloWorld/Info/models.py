from __future__ import unicode_literals

from django.db import models
# Create your models here.
from ..Account.models import Address, Account


class CreditCard(models.Model):
	number = models.IntegerField()
	expire_date = models.DateField()
	cvv = models.IntegerField()
	address = models.ForeignKey(Address)
	owner = models.ForeignKey(Account, on_delete=models.CASCADE)