from django.db import models
from django.contrib.auth.models import User

from stocks.models import Stock

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    price_per_share = models.DecimalField(max_digits=12, decimal_places=4)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_fee = models.DecimalField(max_digits=12, decimal_places=4)
    
    def __str__(self):
        return f"{self.transaction_type} {self.quantity} shares of {self.stock.symbol} at {self.price_per_share} on {self.transaction_date}"