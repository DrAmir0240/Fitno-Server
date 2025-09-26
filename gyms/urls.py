from django.urls import path

from gyms import views

urlpatterns = [
    # <=================== Customer Views ===================>
    path('customer/gyms/', views.CustomerPanelGymList.as_view(), name='customer-gym-list'),
    path('customer/gyms/signed/', views.CustomerPanelCurrentGymDetail.as_view(), name='customer-gym-list-signed'),
    path('customer/gyms/enter-request/', views.CustomerPanelRequestGymEntry.as_view(),
         name='customer-gym-enter-request'),
    path('customer/memberships/', views.CustomerMembershipListView.as_view(), name='customer-membership-list'),
    path('customer/memberships/sign-up/', views.CustomerMembershipSignUp.as_view(),
         name='customer-membership-sign-up'),
]
