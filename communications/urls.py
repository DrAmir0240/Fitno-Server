from django.urls import path

from communications import views

urlpatterns = [
    # <=================== Customer Views ===================>
    path('customer/announcements/gym/', views.CustomerPanelAnnouncementGym.as_view(),
         name='customer-gym-announcement-list'),
    path('customer/announcements/platform/', views.CustomerPanelAnnouncementPlatform.as_view(),
         name='customer-platform-announcement-list'),
    path('customer/tickets/', views.CustomerPanelTicketListCreate.as_view(),
         name='customer-tickets'),
    path('customer/notifications/', views.CustomerPanelNotificationList.as_view(),
         name='customer-notifications'),
]
