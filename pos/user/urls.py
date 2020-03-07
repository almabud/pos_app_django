from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('add_employee/', views.AddEmployeeView.as_view(), name="add_employee")
]
