from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import NotFound
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from accounts.auth import CustomJWTAuthentication
from gyms.models import MemberShip
from communications.models import Announcement, Ticket, Notification
from communications.serializers import AnnouncementSerializer, CustomerPanelTicketSerializer, \
    CustomerPanelNotificationSerializer


# Create your views here.
class CustomerPanelAnnouncementGym(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        customer = getattr(user, "customer", None)
        if not customer:
            raise NotFound("مشتری یافت نشد یا کاربر مشتری نیست.")

        active_memberships = MemberShip.objects.filter(
            customer=customer,
            session_left__gt=0,
        ).filter(
            Q(validity_date__isnull=True) | Q(validity_date__gte=now().date())
        )

        gyms_with_active_memberships = active_memberships.values_list("gym_id", flat=True)

        qs = Announcement.objects.filter(
            type="gym",
            gym_id__in=gyms_with_active_memberships
        ).order_by("-id")

        if not qs.exists():
            raise NotFound("هیچ اطلاعیه باشگاهی برای این کاربر یافت نشد.")

        return qs


class CustomerPanelAnnouncementPlatform(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        qs = Announcement.objects.filter(
            type="platform"
        ).order_by("-id")

        if not qs.exists():
            raise NotFound("هیچ اطلاعیه پلتفرمی یافت نشد.")

        return qs


class CustomerPanelTicketListCreate(generics.ListCreateAPIView):
    serializer_class = CustomerPanelTicketSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        qs = Ticket.objects.filter(sender=user, replied_to__isnull=True).order_by("-send_time")
        # فقط تیکت‌های اصلی کاربر (نه ریپلای‌هایی که خودش زده) رو میاره
        if not qs.exists():
            raise NotFound("هیچ تیکتی برای این کاربر یافت نشد.")
        return qs

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class CustomerPanelNotificationList(generics.ListAPIView):
    serializer_class = CustomerPanelNotificationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        qs = Notification.objects.filter(user=user).order_by("-id")
        if not qs.exists():
            raise NotFound("هیچ نوتیفیکیشنی برای این کاربر یافت نشد.")
        return qs


class CustomerPanelNotificationDetail(generics.RetrieveAPIView):
    serializer_class = CustomerPanelNotificationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=["is_read"])
        return obj
