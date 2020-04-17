import json

from django.db.models import Prefetch
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

# from product.models import ProductTransaction
from django.views.generic import FormView, TemplateView

from product.forms import AddNewProductForm, AddNewSupplierForm, OrderForm, ItemForm, BaseItemFormSet
from product.models import Product, Supplier, Customer, Order
from scripts.pos_invoice_genarator import generate_pos_invoice


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


class CustomerList(View):
    def get(self, request):
        return render(request, 'product/customer_list.html', {"customer_list": Customer.objects.get_all_customer()})


class OrderList(View):
    def get(self, request):
        return render(request, 'product/order_list.html', {"order_list": Order.objects.get_all_order()})


class CreateInvoice(TemplateView):
    template_name = 'product/create_invoice.html'
    ItemFormSet = formset_factory(ItemForm, formset=BaseItemFormSet, extra=0)

    def get_context_data(self, **kwargs):
        product_list = Product.objects.get_all_product_stock_filter()
        if 'items' not in kwargs:
            kwargs['items'] = self.ItemFormSet()

        if 'order' not in kwargs:
            kwargs['order'] = OrderForm()

        kwargs['product_list'] = product_list

        return super().get_context_data(**kwargs)

    def post(self, request):
        item_formset = self.ItemFormSet(request.POST)
        order_form = OrderForm(request.POST)
        if order_form.is_valid() and item_formset.is_valid():
            order = order_form.cleaned_data
            items = item_formset.cleaned_data
            order['sold_by'] = request.user
            created_order = Order.objects.crate_new_order(order=order, items=items)
            return self.render_to_response(self.get_context_data(pos_invoice=generate_pos_invoice(created_order), order_id=created_order.id))
        else:
            # for field in order_form:
            #     for error in field.errors:
            #         print(error)
            return self.render_to_response(self.get_context_data(order=order_form, selected_items=item_formset.cleaned_data))
