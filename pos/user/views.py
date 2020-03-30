from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import DatabaseError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.dateparse import parse_date
from django.views.generic import TemplateView, FormView, RedirectView
from django.contrib.auth import authenticate, login, logout, get_user_model

from user.forms import LoginForm

from scripts.mixin import LoggedOutRequiredMixin

from user.forms import AddNewEmployeeForm


class LoginView(LoggedOutRequiredMixin, FormView):
    template_name = "user/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('dashboard:dashboard')
        return redirect('user:login')


class LogoutView(RedirectView):
    permanent = True
    query_string = False
    pattern_name = 'user:login'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class AddEmployeeView(FormView, LoginRequiredMixin):
    template_name = 'user/create_user.html'
    form_class = AddNewEmployeeForm

    def form_valid(self, form):
        extra_field = form.cleaned_data
        try:
            user = get_user_model().objects.create_user(**extra_field)
        except DatabaseError:
            return HttpResponse(DatabaseError.message)
        return HttpResponse(user)

    # def post(self, request, *args, **kwargs):
    #     #     request.POST._mutable = True
    #     #     value = request.POST
    #     #     value['dob'] = datetime.strptime(value['dob'], "%m-%d-%Y").date()
    #     #     form = self.form_class(value)
    #     #     if form.is_valid():
    #     #         try:
    #     #             user = get_user_model().objects.create_user(**form.cleaned_data)
    #     #             print(user)
    #     #         except DatabaseError:
    #     #             return HttpResponse(DatabaseError.message)
    #     #         return HttpResponse('/success/')
    #     #     else:
    #     #
    #     #         print(form.errors)
    #     #         return HttpResponse(form.errors)
