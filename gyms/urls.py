from django.urls import path
from gyms import views

urlpatterns = [
    # <=================== Customer Views ===================>
    path('customer/gyms/', views.CustomerPanelGymList.as_view(), name='customer-gym-list'),
    path('customer/gyms/<int:pk>/', views.CustomerPanelGymDetail.as_view(), name='customer-gym-detail'),
    path('customer/gyms/signed/', views.CustomerPanelCurrentGymList.as_view(), name='customer-gym-list-signed'),
    path('customer/gyms/signed/<int:pk>/', views.CustomerPanelCurrentGymDetail.as_view(), name='customer-gym-signed'),
    path('customer/gyms/enter-request/', views.CustomerPanelRequestGymEntry.as_view(),
         name='customer-gym-enter-request'),
    path('customer/memberships/', views.CustomerPanelMembershipListView.as_view(), name='customer-membership-list'),
    path('customer/memberships/<int:pk>/', views.CustomerPanelMembershipDetailView.as_view(),
         name='customer-membership-detail'),
    path('customer/memberships/sign-up/', views.CustomerMembershipSignUp.as_view(),
         name='customer-membership-sign-up'),
    # <=================== Gym Views ===================>
    path('gym-panel/gyms/<int:pk>/', views.GymPanelGymEdit.as_view(), name='gym-panel-gym-detail'),

]
