from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

# from product.models import ProductTransaction
from django.views.generic import FormView, TemplateView

from product.forms import AddNewProductForm, AddNewSupplierForm, OrderForm, ItemForm, BaseItemFormSet
from product.models import Product, Supplier, Customer, Order


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
    item_formset = ItemFormSet()
    order_form = OrderForm()
    product_list = Product.objects.get_all_product()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.order_form)
        context['order'] = self.order_form
        context['items'] = self.item_formset
        context['product_list'] = self.product_list
        return context

    def post(self, request):
        self.item_formset = self.ItemFormSet(request.POST)
        self.order_form = OrderForm(request.POST)
        print(self.order_form)
        if self.order_form.is_valid() and self.item_formset.is_valid():
            pass
        else:
            return render(template_name=self.template_name, context={'order': self.order_form,
                                                                     'items': self.item_formset,
                                                                     'product_list': self.product_list},
                          request=request)
