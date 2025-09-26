from rest_framework import serializers
from communications.models import Announcement, Ticket, Notification


class AnnouncementSerializer(serializers.ModelSerializer):
    gym_title = serializers.CharField(source="gym.title", read_only=True)
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)

    class Meta:
        model = Announcement
        fields = ["id", "type", "message", "gym_title", "sender_name"]


class CustomerPanelRecursiveTicketSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = CustomerPanelTicketSerializer(instance, context=self.context)
        return serializer.data


class CustomerPanelTicketSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)
    replies = CustomerPanelRecursiveTicketSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "sender_name", "message", "send_time", "replies", "replied_to"]
        extra_kwargs = {
            "replied_to": {"write_only": True, "required": False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        ticket = Ticket.objects.create(sender=user, **validated_data)
        return ticket


class CustomerPanelNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "action", "message", "is_read", "meta"]
