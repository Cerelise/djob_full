
from company.models import Company
from company.serializers import CompanySerializer
from core.handler import APIResponse
from django.utils.timezone import now
from notification.models import Notification
from notification.utils import create_notification
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView


class VerifyCompany(APIView):
  
    permission_classes = [IsAdminUser]
    
    def post(self,request,pk):

        data = request.data

        company_status = data['status']

        verified_company = Company.objects.filter(id=pk).update(
          status=company_status,
        )

        original_notice = Notification.objects.filter(company=pk).first()

        if company_status == 1:
            notification = create_notification(request,'accept_company_request',company_id=pk)
            notification.notification_status = 1
            notification.save()
            original_notice.notification_status = 1
            notification.save()
        elif company_status == 2:
            notification = create_notification(request,'reject_company_request',company_id=pk)
            notification.notification_status = 2
            notification.save()
            original_notice.notification_status = 2
            notification.save()

        company_detail = Company.objects.get(id=pk)
        company_detail.created_at = now()
        company_detail.save()

        company_serializer = CompanySerializer(company_detail)

        

        return APIResponse(code=200,msg='申请已处理！',data=company_serializer.data)