from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from account.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(unique=True, max_length=255)
	full_name = models.CharField(max_length=255, blank=True)
	contact = models.CharField(max_length=20, blank=True)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

	is_active = models.BooleanField(default=True)
	is_verified = models.BooleanField(default=False)
	is_google_user = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['full_name']

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'
		ordering = ['-created_at']

	def __str__(self):
		return self.email
