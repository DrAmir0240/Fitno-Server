from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import User


# Create your models here.
class Transaction(models.Model):
    payer_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='payer_transactions',
                                           null=True)
    payer_object_id = models.PositiveIntegerField(null=True)
    payer = GenericForeignKey('payer_content_type', 'payer_object_id')

    receiver_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                              related_name='receiver_transactions', null=True)
    receiver_object_id = models.PositiveIntegerField(null=True)
    receiver = GenericForeignKey('receiver_content_type', 'receiver_object_id')

    payment_method = models.CharField(
        max_length=100,
        choices=(('online', 'آنلاین'), ('cash', 'نقدی')),
        default='online'
    )
    online_transaction = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(default=0)
    is_commission = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Tx {self.id} - {self.price}"
