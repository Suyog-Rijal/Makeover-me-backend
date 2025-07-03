from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	ordering = ['-created_at']
	list_display = ['email', 'full_name', 'is_active', 'is_verified', 'is_google_user']
	list_filter = ['is_active', 'is_staff', 'is_google_user', 'is_verified']

	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		(_('Personal info'), {'fields': ('full_name', 'contact')}),
		(_('Permissions'), {'fields': (
			'is_active', 'is_staff', 'is_superuser', 'is_verified', 'is_google_user', 'groups', 'user_permissions')}),
		(_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': (
				'email', 'full_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'is_verified'),
		}),
	)

	search_fields = ['email', 'full_name']
