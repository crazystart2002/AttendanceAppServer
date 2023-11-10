from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ["id", "role", "email", "name", "is_admin", "username"]
    list_filter = ["is_admin"]
    fieldsets = [
        ('User Credentials', {"fields": ["username", "password"]}),
        ("Personal info", {"fields": ('name', 'tc', 'email')}),
        ("Permissions", {"fields": ("is_admin",)}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "email", "name", "role", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["username"]
    ordering = ["username", "id"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)

