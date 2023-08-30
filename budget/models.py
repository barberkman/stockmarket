from django.db import models
from django.contrib.auth.models import User

from stocks.models import Currency


class Budget(models.Model):
    user = models.OneToOneField(
        to='auth.User',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    money = models.DecimalField(max_digits=12, decimal_places=4)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} : {self.money} {self.currency.symbol}"
    