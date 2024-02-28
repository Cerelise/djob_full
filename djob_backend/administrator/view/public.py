from company.models import Company
from company.serializers import CompanySerializer
from core.handler import APIResponse
from django.db.models import Q
from jobs.models import Job
from jobs.serializers import JobSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes


class FilterRecruitDataView(APIView):

    permission_classes = [IsAdminUser]
    
    def get(selt,request):
        # print(request)
        if request.GET.get('keyword',''):
            keyword = request.GET.get('keyword','')
        else :
            keyword = 'company'
        

        if keyword == 'company':
            listing = Company.objects.filter(status=0)
            serializer = CompanySerializer(listing,many=True)
            data = serializer.data
        elif keyword == 'job':
            listing = Job.objects.filter(status=0)
            serializer = JobSerializer(listing,many=True)
            data = serializer.data
        elif keyword == 'all':        
            listing_company = Company.objects.filter(Q(status=1) | Q(status=2))
            
            listing_job = Job.objects.filter(Q(status=1) | Q(status=2))
            serializer_company = CompanySerializer(listing_company,many=True)
            serializer_job = JobSerializer(listing_job,many=True)

            company_data = serializer_company.data
            job_data = serializer_job.data
            merged_data = company_data + job_data
            data = merged_data
            
        return APIResponse(code=200,msg='',data=data)
    

# @api_view('GET')
# @permission_classes([IsAdminUser])
# def getNotification()