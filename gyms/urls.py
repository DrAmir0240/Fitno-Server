from django.urls import path

from gyms import views

urlpatterns = [
    # <=================== Customer Views ===================>
    path('customer/gyms/', views.CustomerPanelGymList.as_view(), name='customer-gym-list'),
    path('customer/gyms/signed/', views.CustomerPanelCurrentGymDetail.as_view(), name='customer-gym-list-signed'),

]
