from django.db import models

class CreditCard(models.Model):
	number = models.IntegerField()
	expire_date = models.DateField()
	cvv = models.IntegerField()
	address = models.ForeignKey('Address')
	owner = models.ForeignKey('Account.Account', on_delete=models.CASCADE)

class Address(models.Model):
	address1 = models.CharField(max_length=200)
	address2 = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=200)
	zip_code = models.IntegerField()
	state = models.CharField(max_length=200)


class Order(models.Model):
	STATUS = (
    	(0, 'Not Shipped'),
    	(1, 'Shipped'),
    	(2, 'Delivered')
  	)
	created = models.DateTimeField(auto_now=True)
	amount = models.IntegerField(default=0)
	item = models.ForeignKey('Item.Item', on_delete=models.CASCADE)
	buyer = models.ForeignKey('Account.Account', related_name='purchased')
	seller = models.ForeignKey('Account.Account', related_name='selled')
	status = models.IntegerField(default=0, choices=STATUS)	


