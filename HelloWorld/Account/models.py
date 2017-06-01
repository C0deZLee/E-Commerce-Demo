from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class AccountManager(BaseUserManager):
	def create_user(self, email, password=None, **kwargs):
		"""
		Creates and saves a User with the given email, username and password.
		"""
		if not email:
			raise ValueError('Users must have a valid email address')

		if not kwargs.get('username'):
			raise ValueError('Users must have a valid username')

		account = self.model(email=self.normalize_email(email), username=kwargs.get('username'))
		account.set_password(password)
		account.save()
		# Create Cart for new registered account
		cart = Cart(user_id = account.id)
		cart.save()
		# Create Account Detail for new registered account		
		deatil = AccountDetail(user_id = account.id)
		deatil.save()
		return account

	def create_superuser(self, email, password, **kwargs):
		account = self.create_user(email, password, **kwargs)
		account.is_admin = True
		account.is_staff = True
		account.is_superuser = True
		account.save()
		return account

class Account(AbstractBaseUser, PermissionsMixin):
	# Basic
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=40, unique=True)

	# permission
	is_admin = models.BooleanField(default=False)
	is_seller = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	# Manager
	objects = AccountManager()
	# Timestamp
	created = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now_add=True)
	# Settings
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	class Meta:
		ordering = ['created']

	def __unicode__(self):
		return self.username

	@property
	def get_full_name(self):
		"Returns the person's full name."
		return self.username

	@property
	def get_short_name(self):
		return self.username

	@property
	def first_name(self):
		"Returns the person's first name."
		return self.username

	@property
	def last_name(self):
		"Returns the person's last name."
		return self.username

class AccountDetail(models.Model):
	user = models.OneToOneField('Account', related_name='detail', unique=True)
	gender = models.CharField(max_length=20, null=True, blank=True)
	mobile = models.IntegerField(null=True, blank=True)
	address = models.ForeignKey('Info.Address', null=True, blank=True)

	def __unicode__(self):
		return self.user.username

class Cart(models.Model):
	user = models.OneToOneField('Account', related_name='cart', unique=True)
	items = models.ManyToManyField('Item.Item', blank=True)

	def __unicode__(self):
		return self.user.username

