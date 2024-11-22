from django.db import models

class BankDetails(models.Model):
    bank_name = models.CharField(max_length=100)
    bank_id = models.CharField(max_length=20, unique=True)  # Make bank_id unique
    mid = models.CharField(max_length=50, unique=True)  # Make mid unique
    merchant_name = models.CharField(max_length=100)
    
    TRANSACTION_TYPES = [
        ('SALE', 'SALE'),
        ('REFUND', 'REFUND'),
        ('NET SETTLED', 'NET SETTLED'),
    ]
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    bank_rule_mapping = models.TextField(null=True, blank=True)  # Nullable field

    class Meta:
        unique_together = ('bank_id', 'mid')  # Unique together constraint to ensure combination is unique

    def __str__(self):
        return f"{self.bank_name} ({self.bank_id})"
