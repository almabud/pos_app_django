from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    template_name = "user/dashboard.html"

