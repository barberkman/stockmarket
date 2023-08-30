from django.views.generic import ListView

from .models import Stock

class StockListView(ListView):
    model = Stock
    template_name = "stock_list.html"
