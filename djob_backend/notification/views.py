from core.handler import APIResponse
from rest_framework.decorators import api_view

from .models import Notification
from .serializers import NotificationSerializer


@api_view(['POST'])
def read_notification(request,pk):
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()
 
    return APIResponse(code=200,msg='通知已被阅读')