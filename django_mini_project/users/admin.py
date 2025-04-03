# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'nickname', 'name', 'is_admin', 'is_staff')
    list_filter = ('is_admin', 'is_staff')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('개인 정보', {'fields': ('nickname', 'name', 'phone_number')}),
        ('권한', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'name', 'phone_number', 'password1', 'password2', 'is_staff', 'is_admin'),
        }),
    )

    search_fields = ('email', 'nickname', 'name')


admin.site.register(User, UserAdmin)