from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import NotFound
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from accounts.auth import CustomJWTAuthentication
from gyms.models import MemberShip
from communications.models import Announcement
from communications.serializers import AnnouncementSerializer


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
