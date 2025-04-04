from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):  # ❌ UserAdmin 사용하면 안 됨
    list_display = ('account_number', 'bank_codes', 'account_type', 'balance', 'user', 'create_at')  # 표시할 필드
    search_fields = ('account_number', 'user__username')  # 검색 가능 필드
    list_filter = ('bank_codes', 'account_type')  # 필터링 옵션
    ordering = ('-create_at',)  # 최신 계좌 순 정렬