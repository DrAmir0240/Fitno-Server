from django.utils.timezone import now
from rest_framework import serializers

from gyms.models import Gym


class CustomerPanelGymSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Gym
        fields = '__all__'  # همه فیلدهای Gym
        # و فیلد status هم اضافه میشه

    def get_status(self, obj):
        request = self.context.get("request")
        customer = getattr(request.user, "customer", None)
        if not customer:
            return "غیر فعال"

        membership = obj.memberships.filter(customer=customer).first()
        if not membership:
            return "غیر فعال"

        # شرط فعال بودن: session_left > 0 و تاریخ اعتبار تموم نشده
        if membership.session_left > 0 and (
            membership.validity_date is None or membership.validity_date >= now().date()
        ):
            return "فعال"
        return "غیر فعال"
