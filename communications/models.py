from django.db import models

from accounts.models import User
from gyms.models import Gym


# Create your models here.
class Ticket(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_tickets')
    message = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)
    replied_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Ticket {self.id} from {self.sender}"


class Notification(models.Model):
    action = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    meta = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Notification for {self.user}"


class Announcement(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements')
    gym = models.ForeignKey(Gym, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements')
    type = models.CharField(max_length=100, choices=(('gym', 'باشگاهی'), ('platform', 'پلتفرم'),),
                            default='gym')
    message = models.TextField()

    def __str__(self):
        return f"Announcement {self.gym.title} from {self.sender.gym_manager.user.full_name}"
