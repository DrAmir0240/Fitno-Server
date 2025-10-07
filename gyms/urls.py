from django.urls import path
from gyms import views

urlpatterns = [
    path('choices/', views.GymChoices.as_view(), name='gym-choices'),

    # <=================== Customer Views ===================>
    path('customer/gyms/', views.CustomerPanelGymList.as_view(), name='customer-gym-list'),
    path('customer/gyms/<int:pk>/', views.CustomerPanelGymDetail.as_view(), name='customer-gym-detail'),
    path('customer/gyms/signed/', views.CustomerPanelSingedGymList.as_view(), name='customer-gym-list-signed'),
    path('customer/gyms/signed/<int:pk>/', views.CustomerPanelSignedGymDetail.as_view(), name='customer-gym-signed'),
    path('customer/gyms/enter-request/', views.CustomerPanelRequestGymEntry.as_view(),
         name='customer-gym-enter-request'),
    path('customer/memberships/', views.CustomerPanelMembershipListView.as_view(), name='customer-membership-list'),
    path('customer/memberships/<int:pk>/', views.CustomerPanelMembershipDetailView.as_view(),
         name='customer-membership-detail'),
    path('customer/memberships/sign-up/', views.CustomerMembershipSignUp.as_view(),
         name='customer-membership-sign-up'),
    path('customer/in-out/', views.CustomerPanelInOutList.as_view(), name='customer-in-out-list'),

    # <=================== Gym Views ===================>
    path('gym-panel/gyms/', views.GymPanelGym.as_view(), name='gym-panel-gym'),
    path('gym-panel/gyms/<int:pk>/', views.GymPanelGymDetail.as_view(), name='gym-panel-gym-detail'),
    path('gym-panel/membership-types/', views.GymPanelMemberShipType.as_view(),
         name='membershiptype'),
    path('gym-panel/membership-types/<int:pk>/', views.GymPanelMemberShipTypeDetail.as_view(),
         name='membershiptype-detail'),
    path('gym-panel/banner/', views.GymPanelGymBanner.as_view(),
         name='banner'),
    path('gym-panel/banner/<int:pk>/', views.GymPanelGymBannerDetail.as_view(),
         name='banner-detail'),
]
