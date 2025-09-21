from django.urls import path

from accounts import views

urlpatterns = [
    # <=================== Customer Views ===================>
    path('customer/register/', views.CustomerRegisterView.as_view(), name='customer-register'),
    path('customer/login/', views.CustomerLoginView.as_view(), name='customer-login'),
    path('customer/logout/', views.CustomerLogoutView.as_view(), name='customer-logout'),

]
