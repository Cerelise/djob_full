from core.handler import APIResponse
from rest_framework.decorators import api_view

from .models import Notification
from .serializers import NotificationSerializer


# 查看通知（提供id）
@api_view(['GET'])
def notifications(request):
    received_notifications = Notification.objects.filter(created_for_id=request.user.id)
    serializer = NotificationSerializer(received_notifications,many=True)
    return APIResponse(code=200,msg="",data=serializer.data)

