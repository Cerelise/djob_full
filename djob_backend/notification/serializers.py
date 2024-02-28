from rest_framework import serializers

from .models import Notification
from accounts.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = ('id','content','type_of_notification','created_by','notification_status','created_at')