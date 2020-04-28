import json
from datetime import datetime

from django.db.models import Prefetch
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

# from product.models import ProductTransaction
from django.views.generic import FormView, TemplateView

from product.forms import AddNewProductForm, AddNewSupplierForm, OrderForm, ItemForm, BaseItemFormSet, ProductForm, \
    VariantForm, NewStockForm
from product.models import Product, Supplier, Customer, Order, ProductVariant
from scripts.pos_invoice_genarator import generate_pos_invoice


class ProductList(TemplateView):
    template_name = 'product/product_list.html'

    def get_context_data(self, **kwargs):
        kwargs['product_list'] = Product.objects.get_all_product()
        return super().get_context_data(**kwargs)

    def post(self, request):
        if request.is_ajax():
            id = request.POST['variant_id']
            if id:
                if ProductVariant.objects.delete_variant(id):
                    return JsonResponse('success', status=200, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            else:
                return JsonResponse('error', status=400, safe=False)


class VariantDetails(TemplateView):
    template_name = 'product/variant_details.html'

    def get_context_data(self, **kwargs):
        variant_id = kwargs['variant_id']
        variant_details = ProductVariant.objects.get_product_variant_details(variant_id)
        product_edit_form = ProductForm(initial={
            'product_name': variant_details.product.product_name,
            'product_description': variant_details.product.product_description
        })
        variant_edit_form = VariantForm(initial={
            'product': variant_details.product,
            'new_product_name': variant_details.product.product_name,
            'product_description': variant_details.product.product_description,
            'gsm': variant_details.gsm,
            'color': variant_details.color,
            'size': variant_details.size,
            'category': variant_details.category,
            'bag_purchase_price': variant_details.bag_purchase_price,
            'marketing_cost': variant_details.marketing_cost,
            'transport_cost': variant_details.transport_cost,
            'printing_cost': variant_details.printing_cost,
            'vat': variant_details.vat,
            'profit': variant_details.profit,
            'discount_percent': variant_details.discount_percent,
            'discount_min_purchase': variant_details.discount_min_purchase,
            'stock_total': variant_details.stock_total
        })
        kwargs['variant_details'] = variant_details
        kwargs['product_form'] = product_edit_form
        kwargs['variant_form'] = variant_edit_form
        kwargs['new_stock_form'] = NewStockForm()
        return super().get_context_data(**kwargs)

    def post(self, request, variant_id):
        if request.is_ajax():
            data = request.POST
            # print(data['id'])
            if 'is_product_edited' in data and data['is_product_edited']:
                form = ProductForm(data)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    Product.objects.update_product(data['id'], cleaned_data)
                    return JsonResponse("success", status=201, safe=False)
                else:
                    return JsonResponse(form.errors, status=400)
            elif 'is_variant_edited' in data and data['is_variant_edited']:
                form = VariantForm(data)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    ProductVariant.objects.update_variant(variant_id, cleaned_data)
                    return JsonResponse("success", status=201, safe=False)
                else:
                    return JsonResponse(form.errors, status=400)
            else:
                form = NewStockForm(data)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    supplier = ProductVariant.objects.add_new_stock(id=variant_id, form_data=cleaned_data)
                    date = datetime.strftime(supplier.date, '%d/%m/%Y %I:%M %p')
                    return JsonResponse({'date': date, 'name': cleaned_data['supplier'].name,
                                         'mobile_no': cleaned_data['supplier'].mobile_no,
                                         'total_supplied': supplier.total_supplied,
                                         'address': cleaned_data['supplier'].address}, status=201)
                else:
                    return JsonResponse(form.errors, status=400)


class ProductDetails(TemplateView):
    template_name = 'product/product_details.html'


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


class SupplierDetail(TemplateView):
    template_name = 'product/supplier_details.html'

    def get_context_data(self, **kwargs):
        supplier_id = kwargs['supplier_id']
        supplier_details = Supplier.objects.get_supplier_details(supplier_id)
        supplier_edit_form = AddNewSupplierForm(initial={'name': supplier_details.name,
                                                         'mobile_no': supplier_details.mobile_no,
                                                         'address': supplier_details.address})
        kwargs['supplier_details'] = supplier_details
        kwargs['form'] = supplier_edit_form
        return super().get_context_data(**kwargs)

    def post(self, request, supplier_id):
        if request.is_ajax():
            data = request.POST
            form = AddNewSupplierForm(data)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                Supplier.objects.update_supplier(id=supplier_id, data=cleaned_data)
                return JsonResponse("success", status=201, safe=False)
            else:
                return JsonResponse(form.errors, status=400)


class CustomerList(View):
    def get(self, request):
        return render(request, 'product/customer_list.html', {"customer_list": Customer.objects.get_all_customer()})


class OrderList(View):
    def get(self, request):
        return render(request, 'product/order_list.html', {"order_list": Order.objects.get_all_order()})

    def post(self, request):
        if request.is_ajax():
            id = request.POST['order_id']
            if id:
                if Order.objects.delete_order(id):
                    return JsonResponse('success', status=200, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            else:
                return JsonResponse('error', status=400, safe=False)


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
            order_details = Order.objects.get_order_detail(created_order.id)
            return self.render_to_response(
                self.get_context_data(pos_invoice=generate_pos_invoice(order_details), order_id=created_order.id))
        else:
            # for field in order_form:
            #     for error in field.errors:
            #         print(error)
            return self.render_to_response(
                self.get_context_data(order=order_form, selected_items=item_formset.cleaned_data))


class OrderDetail(TemplateView):
    template_name = 'product/order_details.html'

    def get_context_data(self, **kwargs):
        order_details = Order.objects.get_order_detail(order_id=self.kwargs['order_id'])
        kwargs['order_details'] = order_details
        kwargs['pos_invoice'] = generate_pos_invoice(order_details)

        return super().get_context_data(**kwargs)

    def post(self, request, order_id):
        if request.is_ajax():
            if 'payment_id' in request.POST:
                id = request.POST['payment_id']
                if id:
                    if Order.objects.delete_payment(id):
                        order_details = Order.objects.get_order_detail(order_id=order_id)
                        pos_invoice = generate_pos_invoice(order_details)
                        return JsonResponse(pos_invoice, status=200, safe=False)
                    else:
                        return JsonResponse('error', status=400, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            elif 'order_item_id' in request.POST:
                id = request.POST['payment_id']
                if id:
                    if Order.objects.delete_order(id):
                        return JsonResponse('success', status=200, safe=False)
                    else:
                        return JsonResponse('error', status=400, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
        current_user = request.user
        new_payment = Order.objects.make_payment(order_id, request.POST['amount'], current_user)
        return HttpResponseRedirect(self.request.path_info)
