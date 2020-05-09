from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from investor.form import InvestorForm, InvestForm
from investor.models import ShareHolder


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
