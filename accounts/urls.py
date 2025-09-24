from django.urls import path

from accounts import views

urlpatterns = [
    # <=================== User Views ===================>
    path('status/', views.UserRoleStatusView.as_view(), name='status'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh-token/', views.RefreshTokenView.as_view(), name='refresh-token'),
    path('test/', views.TestView.as_view(), name='test'),

    # <=================== Customer Views ===================>
    path('customer/register/', views.CustomerRegisterView.as_view(), name='customer-register'),
    # <=================== GymManager Views ===================>
    path('gym-manager/upgrade/', views.GymManagerCreateView.as_view(), name='gym-manager-upgrade'),
    path('gym-manager/add-gym/', views.GymCreateView.as_view(), name='add-gym'),

]
