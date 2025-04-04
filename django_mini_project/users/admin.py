from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    ordering = ('email',)  # UUID 기반 정렬

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('개인 정보', {'fields': ('name', 'phone_number')}),
        ('권한 설정', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone_number', 'password'),
        }),
    )

    search_fields = ('email', 'name', 'phone_number')


admin.site.register(CustomUser, CustomUserAdmin)