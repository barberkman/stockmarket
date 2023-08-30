from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Transaction


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transaction_list.html"
    ordering = ["-transaction_date"]
