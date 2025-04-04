from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser

    list_display = ('email', 'name', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    search_fields = ('email', 'name', 'phone_number')
    ordering = ('email',)

    readonly_fields = ('is_staff',)  # ✅ 어드민 여부는 읽기 전용

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

admin.site.register(CustomUser, CustomUserAdmin)