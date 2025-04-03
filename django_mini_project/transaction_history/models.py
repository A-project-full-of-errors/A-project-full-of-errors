import uuid
from django.db import models
from accounts.models import Account

class TransactionHistory(models.Model):
    transaction_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='transaction_id'
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        db_column='account_id',
        related_name='transaction_histories'
    )
    # 거래 금액
    transaction_amount = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_column='transaction_amount'
    )

    # 거래 상세 내용
    transaction_details = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column='transaction_details'
    )
    # 거래 타입
    transaction_type = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        db_column='transaction_type'
    )
    # 거래 시간
    transaction_date = models.DateTimeField(
        null=True,
        blank=True,
        db_column='transaction_date'
    )
    # 잔액
    after_balance = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_column='after_balance'
    )

    # 거래 방법
    transaction_method = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        db_column='transaction_method'
    )

    def __str__(self):
        return f"{self.account} - {self.transaction_type} - {self.transaction_amount}"

    class Meta:
        db_table = 'transaction_history'
