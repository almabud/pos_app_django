import copy
import json
from datetime import datetime
from json import JSONEncoder

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Sum, F, QuerySet
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime, now
from django.views.generic import TemplateView

from investor.form import InvestorForm, InvestForm
from investor.models import ShareHolder, InvestHistory
from product.models import OrderedItem


class InvestorList(TemplateView):
    template_name = 'investor/investor.html'

    def get_context_data(self, **kwargs):
        kwargs['investors'] = ShareHolder.objects.all_investor()
        kwargs['investor_form'] = InvestorForm()
        kwargs['invest_form'] = InvestForm()
        return super().get_context_data(**kwargs)

    def post(self, request):
        data = request.POST
        if request.is_ajax():
            if 'dlt_id' in data:
                if ShareHolder.objects.release_investor(data['dlt_id']):
                    return JsonResponse("success", status=201, safe=False)
                else:
                    return JsonResponse("error", status=400, safe=False)
            else:
                investor_form = InvestorForm(data)
                invest_form = InvestForm(data)
                if not investor_form.is_valid() and not investor_form.is_valid():
                    return JsonResponse([investor_form.errors, invest_form.errors], status=400, safe=False)
                elif not invest_form.is_valid():
                    return JsonResponse(invest_form.errors, status=400)
                elif not investor_form.is_valid():
                    return JsonResponse(investor_form.errors, status=400)
                if investor_form.is_valid() and invest_form.is_valid():
                    investor_data = investor_form.cleaned_data
                    invest_data = invest_form.cleaned_data
                    investor_data.update(**invest_data)
                    new_investor = ShareHolder.objects.create_investor(data)
                    new_investor_data = {
                        'id': new_investor.id,
                        'joining_date': datetime.strftime(new_investor.joining_date, '%d/%m/%Y'),
                        'name': new_investor.name,
                        'phone_no': new_investor.phone_no,
                        'address': new_investor.address
                    }
                    return JsonResponse(new_investor_data, status=201, safe=False)
                return JsonResponse("error", status=400)


class JsonSerializer(JSONEncoder):
    def default(self, obj):
        data = {
            'id': obj.id,
            'amount': obj.amount,
            'date': datetime.strftime(obj.date, '%d/%m/%Y %I:%M %p'),
            'profit': obj.profit,
            'profit_percent': obj.profit_percent
        }
        return data


class ShareholderDetails(TemplateView):
    template_name = 'investor/investor_details.html'

    def get_context_data(self, **kwargs):
        id = kwargs['shareholder_id']
        cur_month = localtime(now()).month
        cur_year = localtime(now()).year
        if cur_month is 1:
            cur_month = 12
            cur_year -= 1
        else:
            cur_month -= 1
        all_month_profit = list(OrderedItem.objects.calculate_profit_revenue_all_month())
        investor_details = ShareHolder.objects.investor_details(id)
        total_profit = 0
        for profit in all_month_profit:
            if profit['order__ordered_date__year'] == now().year and profit[
                'order__ordered_date__month'] == now().month:
                continue
            max_date = now()
            if profit['order__ordered_date__month'] is 12:
                max_date = max_date.replace(year=max_date.year + 1, month=1, day=1)
            else:
                max_date = max_date.replace(month=profit['order__ordered_date__month'] + 1, day=1)

            investor_profit = InvestHistory.objects.calculate_shareholder_profit(net_profit=profit['net_profit'],
                                                                                 invest_history=investor_details.invest_history,
                                                                                 invest_max_date=max_date)
            profit['invest_history'] = json.dumps(copy.deepcopy(investor_profit['invest_history']),
                                                             cls=JsonSerializer)
            # profit['invest_history'] = copy.deepcopy(investor_profit['invest_history'])
            profit['this_month_profit'] = investor_profit['total_profit']
            profit['this_month_profit_percent'] = (investor_profit['total_profit'] * 100.0) / profit['net_profit']
            total_profit += investor_profit['total_profit']
            if profit['order__ordered_date__year'] == cur_year and profit[
                'order__ordered_date__month'] == cur_month:
                investor_details.latest_profit = investor_profit['total_profit']
                investor_details.latest_profit_percent = profit['this_month_profit_percent']

        investor_details.total_earning = total_profit
        kwargs['investor_form'] = InvestorForm(initial={
            'name': investor_details.name,
            'phone_no': investor_details.phone_no,
            'address': investor_details.address
        })
        kwargs['invest_form'] = InvestForm()
        kwargs['investor_details'] = investor_details
        kwargs['profit_details'] = all_month_profit

        return super().get_context_data(**kwargs)

    def post(self, request, shareholder_id):
        if request.is_ajax():
            data = request.POST
            investor = None
            if 'id' in data:
                investor = get_object_or_404(ShareHolder, pk=data['id'])
                investor_form = InvestorForm(data, instance=investor)
            else:
                investor_form = InvestorForm(data)
            invest_form = InvestForm(data)
            if 'dlt_id' in data:
                if InvestHistory.objects.release_invest(data['dlt_id']):
                    return JsonResponse('success', status=201, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            elif investor_form.is_valid():
                if investor_form.save():
                    return JsonResponse('success', status=201, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            elif invest_form.is_valid():
                data = invest_form.cleaned_data
                data['share_holder'] = investor
                created_invest = InvestHistory.objects.create_invest(data)
                result = {
                    'id': created_invest.id,
                    'date': datetime.strftime(created_invest.date, '%d/%m/%Y %I:%M %p'),
                    'amount': created_invest.amount
                }
                return JsonResponse(result, status=201)
            else:
                if not investor_form.is_valid() and not invest_form.is_valid():
                    return JsonResponse({'investor_error': investor_form.errors, 'invest_error': invest_form.errors},
                                        status=400)
                elif not invest_form.is_valid():
                    return JsonResponse(invest_form.errors, status=400)
                if not investor_form.is_valid():
                    return JsonResponse(investor_form.errors, status=400)
