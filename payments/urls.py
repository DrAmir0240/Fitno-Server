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

    # <=================== Admin Views ===================>
    path('admin-panel/transactions/in/', views.AdminPanelInTransactionList.as_view(),
         name='admin-in-transactions'),
    path('admin-panel/transactions/out/', views.AdminPanelOutTransactionList.as_view(),
         name='admin-out-transactions'),
    path('admin-panel/transactions/commissions/', views.AdminPanelCommissionTransactionList.as_view(),
         name='admin-out-transactions'),
    path('admin-panel/transactions/<int:pk>/', views.AdminPanelTransactionDetail.as_view(),
         name='admin-transaction-detail'),

]
