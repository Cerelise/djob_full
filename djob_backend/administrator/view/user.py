from accounts.models import UserAccount
from accounts.serializers import SignUpSerializer, UserSerializer
from core.handler import APIResponse
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


# 分页函数
def AccountPaginator(page):
    paginator = PageNumberPagination()
    paginator.page_size = page
    return paginator

# 用户管理(管理员)类视图
class UserListView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    # 自定义筛选
    def get(self,request):
        if request.GET.get('name','') and request.GET.get('type',''):
            keyword_name = request.GET.get('name','')
            keyword_type = request.GET.get('type','')
            args = {'name__icontains':keyword_name}
            filter_user = UserAccount.objects.filter(**args)
            if len(filter_user) == 0:
                return Response({"message":f"没有找到包含{keyword_name}的用户"},status=status.HTTP_200_OK)
            if keyword_type == "superuser":
                user_list = UserAccount.objects.filter(is_superuser=True,**args)
            elif keyword_type == "employer":
                user_list = UserAccount.objects.filter(is_employer=True,**args)
            else:
                user_list = UserAccount.objects.filter(is_superuser=False,is_employer=False,**args)
        elif request.GET.get('name',''):
              keyword_name = request.GET.get('name','')
              args = {'name__icontains':keyword_name}
              user_list = UserAccount.objects.filter(**args)

              if len(user_list) == 0:
                  return Response({"message":f"没有找到包含{keyword_name}的用户"},status=status.HTTP_200_OK)
        elif request.GET.get('type',''):
            keyword_type = request.GET.get('type','')
            if keyword_type == "superuser":
                user_list = UserAccount.objects.filter(is_superuser=True)
            elif keyword_type == "employer":
                user_list = UserAccount.objects.filter(is_employer=True)
            else:
                user_list = UserAccount.objects.filter(is_superuser=False,is_employer=False)
        else:
            user_list = UserAccount.objects.all()
        pageinator = AccountPaginator(page=5)
        queryset = pageinator.paginate_queryset(user_list,request)
        serializer = UserSerializer(queryset,many=True)
        response = {
          'count':pageinator.page.paginator.count,
          'data':serializer.data
        }
        return APIResponse(code=200,data=response)
    # 新建用户(管理员)
    def post(self,request):
        data = request.data.copy()
        data['email'] = data['email'].lower()
        password = data['password']
        hashed_password = make_password(password)
        data['password'] = hashed_password
        serializer = SignUpSerializer(data=data)
        if serializer.is_valid():
            new_user = serializer.save()
            if new_user.is_employer:
                message = "招聘者创建成功！",
            elif not new_user.is_employer:
                message = "普通用户创建成功！",
            return APIResponse(code=200,msg=message)
        return APIResponse(code=400,msg=serializer.errors)

# 管理员 更新用户
class UserManagerView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get(self,request,pk):
        user_detail = get_object_or_404(UserAccount,id=pk)
        user_serializer = self.serializer_class(instance=user_detail)
        return Response(
          {'data':user_serializer.data},
          status=status.HTTP_200_OK
        )

    def put(self,request,pk):
        user_detail = get_object_or_404(UserAccount,id=pk)
        data = request.data
        password = data['password']
        hashed_password = make_password(password)
        user_data = {
          "name":data['name'],
          "phone":data['phone'],
          "password":hashed_password,
          "description":data['description'],
          "is_employer":data['is_employer'],
          "gender":data['gender'],
        }
        user = UserAccount.objects.filter(id=pk)
        user.update(**user_data)
        user_detail = UserAccount.objects.get(id=pk)
        user_serializer = UserSerializer(user_detail)
        response = {
          "message":"用户信息更新成功！",
          "data":user_serializer.data
        }

        return Response(data=response,status=status.HTTP_200_OK)
        
    
    def delete(self,request,pk):
        user = get_object_or_404(UserAccount,id=pk)        
        user.delete()
        response = {
          "message":"用户删除成功！"
        }
        return Response(data=response,status=status.HTTP_200_OK)


# 获取招聘者列表函数
@api_view(['GET'])
def getEmployer(request):
    employer_list = UserAccount.objects.filter(is_employer=True)
    employer_email = employer_list.values_list('email',flat=True)
    employer_id = employer_list.values_list('id',flat=True)

    combined_data = []
    for id,email in zip(employer_id,employer_email):
        combined_data.append({"id":id,"email":email})
    return APIResponse(code=200,msg="",data=combined_data)