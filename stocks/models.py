from django.db import models


class Currency(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    last_price = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    last_price_date = models.DateTimeField(auto_now=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.symbol} : {self.name}"
