from django.urls import path

from investor import views

app_name = 'investor'
urlpatterns = [
    path('', views.InvestorList.as_view(), name='investors'),
    path('shareholder_details/<int:shareholder_id>', views.ShareholderDetails.as_view(), name='shareholder_details'),
]
