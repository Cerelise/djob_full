import os
import uuid

from core.handler import APIResponse
from django.shortcuts import get_object_or_404
from notification.utils import create_notification
from PIL import Image
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from .models import Company
from .permissions import IsEmployerOrReadOnly
from .serializers import CompanySerializer


def handle_single_photo(file):
    
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10],ext)

    pic_path = os.path.join("media","company","logo",file_name)
    
    os.makedirs(os.path.dirname(pic_path), exist_ok=True)

    img = Image.open(file)

    img.save(pic_path)

    return pic_path

@api_view(['POST'])
def uploadCompanyPhoto(request):
    user = request.user
    if not user.is_employer:
        return APIResponse(code=403,msg="该用户没有足够权限执行该操作，请联系管理员")
    
    picture = request.data

    picture_path = handle_single_photo(picture['logo'])

    response = picture_path.replace('\\','/')

    return APIResponse(code=200,msg='',data=response)


class CompanyListingView(APIView):

    permission_classes = []

    serializer_class = CompanySerializer

    def get(self,request):
        pass

    def post(self,request):
        user = request.user

        if not user.is_employer:
            return APIResponse(code=403,msg='该用户没有足够权限执行该操作，请联系管理员')
        data = request.data
        employer = request.user.id
        data['employer'] = employer
        
        serializer = CompanySerializer(data=data)

        if serializer.is_valid():
            company = serializer.save()

            notification = create_notification(request,'new_company_request',company_id=company.id)

            return APIResponse(code=200,msg="企业信息提交成功！请等待管理员审核！",data=serializer.data)
        return APIResponse(code=400,msg="信息填写错误，请重新填写！")

@api_view(['GET'])
@permission_classes([])
def getCompanyDetails(request):
     user_id = request.user.id
     try:
         company = get_object_or_404(Company,employer=user_id,status=1)
         company_serializer = CompanySerializer(instance=company)

         return APIResponse(code=200,msg="",data=company_serializer.data)
     except:
         return APIResponse(code=200,msg="")


class CompanyManagerView(APIView):
    
    permission_classes = [IsEmployerOrReadOnly]

    serializer_class = CompanySerializer

    def get(self,request,pk):
        company = get_object_or_404(Company,employer=pk)
        company_serializer = self.serializer_class(instance=company)

        return APIResponse(code=200,msg='',data=company_serializer.data)


    def put(self,request,pk):
        company = get_object_or_404(Company,id=pk)
        self.check_object_permissions(request,company)
        data = request.data
        employer = request.user.id
        data['employer'] = employer

        serializer = self.serializer_class(instance=company,data=data)

        if serializer.is_valid():
            company = serializer.save()
            updated_company = Company.objects.filter(id=company.id).update(
              status=0,message=""
            )
            notification = create_notification(request,'new_company_request',company_id=company.id)

            return APIResponse(code=200,msg="新企业信息已提交！请等待管理员审核！")
        return APIResponse(code=400,msg="信息填写错误，请重新填写！")

    def delete(self,request,pk):
          company = get_object_or_404(Company,id=pk)
          self.check_object_permissions(request,company)

          company.delete()

          return APIResponse(code=200,msg="该企业信息已删除!")


