from company.models import Company
from company.serializers import CompanySerializer
from core.handler import APIResponse
from django.db.models import Q
from jobs.models import Job
from jobs.serializers import JobSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView


class FilterRecruitDataView(APIView):
    permission_classes = [IsAdminUser]
    def get(selt,request):
        if request.GET.get('keyword',''):
            keyword = request.GET.get('keyword','')
        else :
            keyword = 'company'
        # 未审核的企业信息
        if keyword == 'company':
            listing = Company.objects.filter(status=0)
            serializer = CompanySerializer(listing,many=True)
            data = serializer.data
        # 未审核的招聘信息
        elif keyword == 'job':
            listing = Job.objects.filter(status=0)
            serializer = JobSerializer(listing,many=True)
            data = serializer.data
        # 已审核的企业信息和招聘信息
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


