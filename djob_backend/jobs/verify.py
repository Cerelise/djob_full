from django.db.models import Q
from notification.utils import create_notification
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Job
from .permissions import IsAdminUserOrReadOnly
from .serializers import JobSerializer


@api_view(['GET'])
def getConditionJob(request,condition):
    
    if condition == '已通过':
        job_list = Job.objects.filter(status=1)
    elif condition == '未通过':
        job_list = Job.objects.filter(~Q(message__isnull=True),status=0)
    elif condition == '未审核':
        job_list = Job.objects.filter(status=0)
    elif condition == '全部':
        job_list = Job.objects.all()

    serializer = JobSerializer(job_list,many=True)

    response = {
      "data":serializer.data
    }
    
    return Response(data=response,status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAdminUserOrReadOnly])
def verifyJob(request,pk):

    data = request.data
    # 0为不通过 1为通过
    job_status = data['status']
    message = data['message']

    verified_job = Job.objects.filter(id=pk).update(
      status=job_status,
      message=message
    )
    if job_status == 1:
        notification = create_notification(request,'accept_job_request',job_id=pk)
    elif job_status == 0 and message:
        notification = create_notification(request,'reject_job_request',job_id=pk)

    job_detail = Job.objects.get(id=pk)

    job_serializer = JobSerializer(job_detail)

    return Response(
      {
        "message":"申请已处理！",
        "detail":job_serializer.data,
      },
      status=status.HTTP_200_OK
    )






   
    



