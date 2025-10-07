from django.urls import path
from payments import views

urlpatterns = [
    # <=================== Customer Views ===================>
    path('customer/transactions/', views.CustomerPanelTransactionsListView.as_view(),
         name='customer-transaction-list'),

    # <=================== Gym Views ===================>
    path('gym-panel/transactions/deposits/', views.GymPanelDepositTransactions.as_view(),
         name='gym-deposits-transactions'),
    path('gym-panel/transactions/withdrawals/', views.GymPanelWithdrawalTransactions.as_view(),
         name='gym-withdrawal-transactions'),
]
