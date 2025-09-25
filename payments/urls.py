from django.urls import path

from payments import views

urlpatterns = [
    # <=================== Customer Views ===================>
    path('customer/transactions/', views.CustomerPanelTransactionsListView.as_view(), name='customer-transaction-list'),

]
