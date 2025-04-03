# Generated by Django 5.1.7 on 2025-04-03 01:33

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TransactionHistory",
            fields=[
                (
                    "transaction_id",
                    models.UUIDField(
                        db_column="transaction_id",
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "transaction_amount",
                    models.PositiveIntegerField(
                        blank=True,
                        db_column="transaction_amount",
                        null=True,
                    ),
                ),

                (
                    "transaction_details",
                    models.CharField(
                        blank=True,
                        db_column="transaction_details",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        blank=True,
                        db_column="transaction_type",
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "transaction_date",
                    models.DateTimeField(
                        blank=True, db_column="transaction_date", null=True
                    ),
                ),
                (
                    "after_balance",
                    models.PositiveIntegerField(
                        blank=True,
                        db_column="after_balance",
                        null=True,
                    ),
                ),
                (
                    "transaction_method",
                    models.CharField(
                        blank=True,
                        db_column="transaction_method",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        db_column="account_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transaction_histories",
                        to="accounts.account",
                    ),
                ),
            ],
            options={
                "db_table": "transaction_history",
            },
        ),
    ]