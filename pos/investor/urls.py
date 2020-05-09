from django.urls import path

from investor import views

app_name = 'investor'
urlpatterns = [
    path('', views.InvestorList.as_view(), name='investors'),
]