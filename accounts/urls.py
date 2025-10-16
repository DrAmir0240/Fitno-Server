from django.urls import path

from accounts import views

urlpatterns = [
    # <=================== User Views ===================>
    path('status/', views.UserRoleStatusView.as_view(), name='status'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('request-otp/', views.RequestOTPView.as_view(), name='request-otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh-token/', views.RefreshTokenView.as_view(), name='refresh-token'),

    # <=================== Customer Views ===================>
    path('customer/register/', views.CustomerRegisterView.as_view(), name='customer-register'),
    path('customer/profile/', views.CustomerProfileView.as_view(), name='customer-profile'),

    # <=================== Gym Views ===================>
    path('gym-manager/upgrade/', views.GymManagerRegisterView.as_view(), name='gym-manager-upgrade'),
    path('gym-manager/add-gym/', views.FirstGymAddView.as_view(), name='add-gym'),
    path('gym-panel/customers/', views.GymPanelCustomerListView.as_view(), name='gym-customers'),
    path('gym-panel/customers/<int:pk>', views.GymPanelCustomerDetailView.as_view(),
         name='gym-customers-detail'),

    # <=================== Admin Views ===================>
    path('admin-panel/customers/', views.AdminPanelCustomerListView.as_view(), name='admin-customers'),
    path('admin-panel/customers/<int:pk>/', views.AdminPanelCustomerDetailView.as_view(),
         name='admin-customers-detail'),

]
