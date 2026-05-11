from django.db import models
from django.core.validators import MaxValueValidator
from apps.clients.models import Client


class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    payer = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='payments',
        db_index=True,
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    percent = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    pay_date = models.DateTimeField(db_index=True)

    class Meta:
        db_table = 'payments'
        indexes = [
            models.Index(fields=['payer', 'pay_date'], name='payment_payer_date_idx'),
        ]

    def __str__(self):
        return f"Payment {self.id} - {self.amount}"
