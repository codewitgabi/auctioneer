from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseAdmin):
	fieldsets = (
		(None, {"fields": ("username", "password")}),
		(_("Personal Info"), {"fields": ("first_name", "last_name", "email", "phone", "image")}),
		(
			_("Permissions"),
			{
				"fields": (
					"is_active",
					"is_staff",
					"is_superuser",
					"groups",
					"user_permissions",
				),
			},
		),
		(_("Important dates"), {"fields": ("last_login", "date_joined")}),
	)
	
	add_fieldsets = (
		(None, {
			"classes": ("wide",),
			"fields": ("username", "email", "password1", "password2")
		}),
	)
	
	list_display = ("id", "username", "email", "phone", "last_login")
	date_hierarchy = "date_joined"
	empty_value_display = "--empty--"
	list_filter = ("date_joined",)
	list_max_show_all = 100
	list_per_page = 100
	ordering = ("username", "-date_joined")
	search_fields = ("username", "email", "phone")
	search_help_text = "Search User..."
	
