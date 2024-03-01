from core.handler import APIResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


@api_view(['GET'])
def notifications(request):

    received_notifications = Notification.objects.filter(created_for_id=request.user.id)
    # print(received_notifications)
    serializer = NotificationSerializer(received_notifications,many=True)

    return APIResponse(code=200,msg="",data=serializer.data)


@api_view(['POST'])
def read_notification(request,pk):
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()
 
    return Response({'message':'该通知已被阅读'})