from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from product.models import ProductVariant, Order, OrderedItem, OtherCost


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    template_name = "user/dashboard.html"

    def get_context_data(self, **kwargs):
        # kwargs['net_stock'] = ProductVariant.objects.net_stock()
        # kwargs['net_order'] = Order.objects.net_order()
        # kwargs['net_sold_item'] = OrderedItem.objects.net_sold_item()
        data = OrderedItem.objects.calculate_net_profit()
        print(data)
        return super().get_context_data(**kwargs)

