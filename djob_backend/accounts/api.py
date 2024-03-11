from datetime import datetime

import redis
from accounts.models import UserAccount
from core.handler import APIResponse
from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .serializers import (SignUpSerializer, UserProfileSerializer,
                          UserSerializer)
from .tokens import create_access_token_for_user
from .validators import validate_file_extension, validate_photo_extension

User = get_user_model()

redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379, db=1,decode_responses=True)

# 注册类视图
class RegisterView(APIView):   
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
    def post(self,request):
        data = request.data

        # 比对验证码
        verify_code = data['code']
        # redis_conn = get_redis_connection()
        stored_code = redis_instance.get(data['email'])
        if stored_code == None:
            return APIResponse(code=400,msg="验证码已过期，请重新获取！")

        if verify_code == stored_code:       
            data['email'] = data['email'].lower()
            user_data = {
                'email':data['email'],
                'password':data['password'],
                'is_employer':data['is_employer']
            }
            serializer = self.serializer_class(data=user_data)           
            if serializer.is_valid():
                is_employer = serializer.validated_data.pop('is_employer', False)
                if is_employer:
                    user = User.objects.create_employer(**serializer.validated_data)
                    message = '招聘者创建成功！'
                else:
                    user = User.objects.create_user(**serializer.validated_data)
                    message = '普通用户创建成功！'
                user.save()
                return APIResponse(code=200,msg=message)
            return APIResponse(code=400,msg="用户名或密码错误",data=serializer.errors)
        else:
            return APIResponse(code=400,msg='验证码有误，请重新输入！')


# 登录类视图
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email,password=password)
        if user is not None:
            user.last_login = datetime.now()
            user.save(update_fields=['last_login'])
            token = create_access_token_for_user(user)
            serializer = UserSerializer(user)
            response = {
                'token':token,
                'user':serializer.data
            }
            return APIResponse(code=200,msg='登录成功',data=response)
        else:
            return APIResponse(code=400,msg='无效的邮箱地址或者密码错误，请重新输入！')

# 修改个人信息类视图
class UserProfileView(APIView):
    permission_classes = []
    def get(self,request):
        user = request.user
        user = UserSerializer(user)
        return APIResponse(code=200,msg="",data=user.data)

    def post(self,request):
        data = request.data 
        user = User.objects.get(id=request.user.id)
        serializer = UserProfileSerializer(data=data,instance=user)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=200,msg="个人信息更改成功",data=serializer.data)
        return APIResponse(code=400,msg="表单填写错误，请重新填写！",data=serializer.errors)

# 上传简历类视图
class UpdateResumeView(APIView):
    permission_classes = []
    def post(self,request):
        user = request.user
        resume = request.FILES['resume']
        if resume == '':
            return APIResponse(code=400,msg='请上传简历！')
        isValidFile = validate_file_extension(resume.name)
        if not isValidFile:
            return APIResponse(code=400,msg="只能上传格式为pdf的文件")
        serializer = UserProfileSerializer(user,many=False)
        current_user = User.objects.get(email=user.email)
        current_user.resume = resume
        current_user.save()
        return APIResponse(code=200,msg="简历更新成功！",data=serializer.data) 

# 上传用户头像函数视图
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UploadAvatar(request):
    user = request.user
    avatar = request.FILES['avatar']
    if avatar == '':
       return APIResponse(code=400,msg='请上传头像！')
    isValidPhoto = validate_photo_extension(avatar.name)
    if not isValidPhoto:
       return APIResponse(code=400,msg="只能上传格式为jpg、png的文件")
    current_user = User.objects.get(email=user.email)
    current_user.avatar = avatar
    current_user.save()
    return APIResponse(code=200,msg="头像已上传！")


@api_view(['GET'])
def getEmployer(request):
    employer_list = UserAccount.objects.filter(is_employer=True)
    employer_email = employer_list.values_list('email',flat=True)
    employer_id = employer_list.values_list('id',flat=True)
    combined_data = []
    for id,email in zip(employer_id,employer_email):
        combined_data.append({"id":id,"email":email})
    return APIResponse(code=200,msg="",data=combined_data)