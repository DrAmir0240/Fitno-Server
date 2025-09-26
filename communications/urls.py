from django.urls import path

from communications import views

urlpatterns = [
    # <=================== Customer Views ===================>
    path('customer/announcements/gym/', views.CustomerPanelAnnouncementGym.as_view(),
         name='customer-gym-announcement-list'),
    path('customer/announcements/platform/', views.CustomerPanelAnnouncementPlatform.as_view(),
         name='customer-platform-announcement-list'),
]
