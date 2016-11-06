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

		account = self.model(
				email=self.normalize_email(email), username=kwargs.get('username')
		)

		account.set_password(password)
		account.save()

		return account

	def create_superuser(self, email, password, **kwargs):
		account = self.create_user(email, password, **kwargs)

		account.is_admin = True
		account.is_superuser = True
		account.save()

		return account


class Address(models.Model):
	address1 = models.CharField(max_length=200)
	address2 = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=200)
	zip_code = models.IntegerField()
	state = models.CharField(max_length=200)


class Account(AbstractBaseUser, PermissionsMixin):
	# Basic
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=40, unique=True)
	gender = models.CharField(max_length=20, null=True, blank=True)
	mobile = models.IntegerField(null=True, blank=True)
	address = models.ForeignKey(Address, null=True, blank=True)
	# permission
	is_admin = models.BooleanField(default=False)
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

	def get_short_name(self):
		return self.username

	def add_friends(self, value):
		pass

	def post_moments(self, value):
		pass

	@property
	def is_staff(self):
		return True


class Seller(models.Model):
	is_enterprise = models.BooleanField(default=False)
	account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='is_seller', primary_key=True)
