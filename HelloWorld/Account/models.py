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
	is_seller = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=True)
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

	@property
	def date_joined(self):
		return self.created

	@property
	def is_active(self):
		return self.is_staff


class CreditCard(models.Model):
	number = models.IntegerField()
	expire_date = models.DateField()
	cvv = models.IntegerField()
	address = models.ForeignKey(Address)
	owner = models.ForeignKey(Account, on_delete=models.CASCADE)