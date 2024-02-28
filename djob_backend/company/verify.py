from django.db.models import Q
from notification.utils import create_notification
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Company
from .permissions import IsAdminUserOrReadOnly
from .serializers import CompanySerializer


@api_view(['GET'])
def getConditionCompany(request,condition):

    if condition == '已通过':
        company_list = Company.objects.filter(status=1)
    elif condition == '未通过':
        company_list = Company.objects.filter(~Q(message__isnull=True),status=0)
    elif condition == '未审核':
        company_list = Company.objects.filter(status=0)
    elif condition == '全部':
        company_list = Company.objects.all()

    serializer = CompanySerializer(company_list,many=True)

    response = {
      "data":serializer.data
    }
    
    return Response(data=response,status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAdminUserOrReadOnly])
def verifyCompany(request,pk):

    data = request.data

    company_status = data['status']
    message = data['message']

    verified_company = Company.objects.filter(id=pk).update(
      status=company_status,
      message=message
    )

    if company_status == 1:
        notification = create_notification(request,'accept_company_request',company_id=pk)
    elif company_status == 0 and message:
        notification = create_notification(request,'reject_company_request',company_id=pk)

    company_detail = Company.objects.get(id=pk)

    company_serializer = CompanySerializer(company_detail)

    return Response(
      {
        "message":"申请已处理！",
        "detail":company_serializer.data
      },
      status=status.HTTP_200_OK
    )