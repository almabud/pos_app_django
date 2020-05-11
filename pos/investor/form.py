from django import forms
from django.forms import TextInput, NumberInput, Textarea, Select

from investor.models import ShareHolder, InvestHistory


class InvestorForm(forms.ModelForm):
    class Meta:
        model = ShareHolder
        fields = ['name', 'phone_no', 'address']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'phone_no': NumberInput(attrs={'class': 'form-control'}),
            'address': Textarea(attrs={'class': 'form-control', 'required': False}),
        }


class InvestForm(forms.ModelForm):
    class Meta:
        model = InvestHistory
        fields = ['amount']
        widgets = {
            'amount': NumberInput(attrs={'class': 'form-control'})
        }
