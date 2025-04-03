from django.db import models
import uuid

class TransactionHistory(models.Model):
    # 거래 ID
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 계좌 ID (ForeignKey로 연결)
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.CASCADE,
        db_column='account_id',
        related_name='transaction_histories',
        null=True  # 임시로 null=True 설정
    )

    # 거래 금액
    transaction_amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='transaction_amount')

    # 거래 세부사항
    transaction_details = models.CharField(max_length=255, db_column='transaction_details')

    # 거래 타입
    transaction_type = models.CharField(max_length=10, db_column='transaction_type')

    # 거래 일시
    transaction_date = models.DateTimeField(auto_now_add=True, db_column='transaction_date')

    # 거래 후 잔액
    after_balance = models.DecimalField(max_digits=18, decimal_places=2, db_column='after_balance')

    # 거래 방법
    transaction_method = models.CharField(max_length=20, db_column='transaction_method')

    def __str__(self):
        return f"{self.account} - {self.transaction_amount} ({self.transaction_type})"

    class Meta:
        db_table = 'transaction_history'
        ordering = ['-transaction_date']
