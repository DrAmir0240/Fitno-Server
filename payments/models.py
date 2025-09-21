from django.db import models

from accounts.models import User


# Create your models here.
class Transaction(models.Model):
    payer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_paid')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='transactions_received')
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    online_transaction = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Tx {self.id} - {self.price}"
