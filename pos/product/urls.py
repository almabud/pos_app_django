from django.urls import path

from product import views

app_name = 'product'
urlpatterns = [
    path('product_list/', views.ProductList.as_view(), name='product_list'),
    path('new_product/', views.AddNewProduct.as_view(), name='new_product'),
    path('new_size/', views.AddNewSize.as_view(), name='new_size'),
    path('new_color/', views.AddNewColor.as_view(), name='new_color'),
    path('new_category/', views.AddNewCategory.as_view(), name='new_category')
]
