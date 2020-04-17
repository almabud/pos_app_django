from django.urls import path

from product import views

app_name = 'product'
urlpatterns = [
    path('product_list/', views.ProductList.as_view(), name='product_list'),
    path('new_product/', views.AddNewProduct.as_view(), name='new_product'),
    path('supplier_list/', views.SupplierList.as_view(), name='supplier_list'),
    path('new_supplier/', views.AddNewSupplier.as_view(), name='new_supplier'),
    path('customer_list/', views.CustomerList.as_view(), name='customer_list'),
    path('order_list/', views.OrderList.as_view(), name='order_list'),
    path('create_invoice/', views.CreateInvoice.as_view(), name='create_invoice'),
    path('order_details/<int:order_id>/', views.OrderDetail.as_view(), name='order_details'),
]
