from typing import Any, Dict
from decimal import Decimal

from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.db.models import Sum, Case, When, IntegerField, DecimalField, F
from django.contrib.auth.mixins import LoginRequiredMixin

from stocks.models import Stock
from transactions.models import Transaction
from .helpers.twelvedatahelper import update_realtime_prices


class PortfolioListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = "portfolio_list.html"
    ordering = ["symbol"]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            buy_sum=Sum(
                Case(
                    When(transaction__transaction_type='BUY', then=F('transaction__quantity') * F('transaction__price_per_share')),
                    default=0,
                    output_field=DecimalField()
                )
            ),
            sell_sum=Sum(
                Case(
                    When(transaction__transaction_type='SELL', then=F('transaction__quantity') * F('transaction__price_per_share')),
                    default=0,
                    output_field=DecimalField()
                )
            ),
            buy_quantity=Sum(
                Case(
                    When(transaction__transaction_type='BUY', then='transaction__quantity'),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            sell_quantity=Sum(
                Case(
                    When(transaction__transaction_type='SELL', then='transaction__quantity'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).annotate(
            net_quantity=F('buy_quantity') - F('sell_quantity'),
            net_sum = F('buy_sum') - F('sell_sum')
        )
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["prices"] = {}
        symbols_list = []
        
        # Get the stock symbols as list
        for object in context["object_list"].all():
            symbols_list.append(object.symbol)
            
        # Update stock model with realtime stock prices
        update_realtime_prices(symbols_list);
        
        # Update context with the prices in the model
        for symbol in symbols_list:
            try:
                stock = Stock.objects.get(symbol=symbol)
                context["prices"][stock.symbol] = stock.last_price
            except:
                pass
            
        return context