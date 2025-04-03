import uuid
from django.db import models
from django.conf import settings


class Account(models.Model):
    account_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='account_id'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='accounts'
    )

    # 계좌 번호
    account_number = models.CharField(max_length=20, null=True, blank=True, db_column='account_number')
    # 은행 코드
    bank_codes = models.CharField(max_length=20, null=True, blank=True, db_column='bank_codes')
    # 계좌 타입
    account_type = models.CharField(max_length=20, null=True, blank=True, db_column='account_type')
    # 잔액
    balance = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True, db_column='balance')

    #생성 및 업데이트 시간
    create_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_column='create_at')
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True, db_column='update_at')

    def __str__(self):
        return f"{self.account_number} ({self.user})"

    class Meta:
        db_table = 'accounts' 
