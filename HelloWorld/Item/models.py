from django.db import models

class Category(models.Model):
	level = models.IntegerField()
	name = models.CharField(max_length=200)
	parentID = models.ForeignKey('self', null=True, blank=True)

	def __unicode__(self):
		return self.name


class Item(models.Model):
	TYPE = (
    	(0, 'Sale'),
    	(1, 'Bid')
  	)

	name = models.CharField(max_length=200)
	keywords = models.CharField(max_length=200)
	provider = models.ForeignKey('Account.Account', on_delete=models.CASCADE)
	description_short = models.CharField(max_length=100, null=True, blank=True)
	description = models.CharField(max_length=1000, null=True, blank=True)
  	type = models.IntegerField(default=0, choices=TYPE)
	category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, related_name='items')

	# For Sale Items
	listed_price = models.FloatField(null=True)
	amount = models.IntegerField(null=True)
	# For Bid Items
	start_time = models.DateTimeField(null=True)
	end_time = models.DateTimeField(null=True)
	reserved_price = models.FloatField(null=True)
	action_price = models.FloatField(null=True)
	current_price = models.FloatField(null=True)
	
	def __unicode__(self):
		return self.name

class Rate(models.Model):
	item = models.ForeignKey(Item, related_name='rates')
	content = models.CharField(max_length=200)
	rater = models.ForeignKey('Account.Account')
	num = models.IntegerField()
	created = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.num)
		