import json

from django.core import serializers
from django.db import IntegrityError
from django.db.models import Prefetch, Sum
from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

# from product.models import ProductTransaction
from django.views.generic import FormView

from product.forms import AddNewProductForm, AddNewSupplierForm
from product.models import Product, Color, Size, Category, Supplier, SupplierTransaction, ProductVariant


class ProductList(View):
    def get(self, request):
        return render(request, 'product/product_list.html', {"product_list": Product.objects.get_all_product()})
        # return HttpResponse(all_products[0].quantity)


class AddNewProduct(FormView):
    template_name = 'product/create_product.html'
    form_class = AddNewProductForm

    def form_valid(self, form):
        clean_form = form.cleaned_data
        Product.objects.create_product(**clean_form)
        return redirect('product:product_list')


class SupplierList(View):
    def get(self, request):
        return render(request, 'product/supplier_list.html', {"supplier_list": Supplier.objects.get_all_supplier()})
        # return HttpResponse(all_products[0].quantity)


class AddNewSupplier(FormView):
    template_name = 'product/create_supplier.html'
    form_class = AddNewSupplierForm

    def form_valid(self, form):
        # clean_form = form.cleaned_data
        supplier = form.save()
        return redirect('product:supplier_list')


class AddNewSize(View):
    def post(self, request):
        try:
            new_size = Size.objects.create(size=request.POST.get('size'))
        except IntegrityError:
            return JsonResponse({'error': 'The value is already exist.'}, status=400)
        return JsonResponse({'size': {'size': new_size.size, 'id': new_size.pk}}, status=201)


class AddNewColor(View):
    def post(self, request):
        try:
            new_color = Color.objects.create(color=request.POST.get('color'))
        except IntegrityError:
            return JsonResponse({'error': 'The value is already exist.'}, status=400)
        return JsonResponse({'color': {'color': new_color.color, 'id': new_color.pk}}, status=201)


class AddNewCategory(View):
    def post(self, request):
        try:
            new_category = Category.objects.create(category=request.POST.get('category'))
        except IntegrityError:
            return JsonResponse({'error': 'The value is already exist.'}, status=400)
        return JsonResponse({'category': {'category': new_category.category, 'id': new_category.pk}}, status=201)