from rest_framework import serializers
from communications.models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    gym_title = serializers.CharField(source="gym.title", read_only=True)
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)

    class Meta:
        model = Announcement
        fields = ["id", "type", "message", "gym_title", "sender_name"]
