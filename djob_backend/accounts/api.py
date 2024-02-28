from datetime import datetime

from accounts.models import UserAccount
from core.handler import APIResponse
from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView

from .serializers import (SignUpSerializer, UserProfileSerializer,
                          UserSerializer)
from .tokens import create_access_token_for_user
from .validators import validate_file_extension, validate_photo_extension

User = get_user_model()

class RegisterView(APIView):

    serializer_class = SignUpSerializer

    def post(self,request):
        data = request.data
        data['email'] = data['email'].lower()
        data['is_employer'] = data['is_employer'] == 'true'
        serializer = self.serializer_class(data=data)
            
        if serializer.is_valid():
            is_employer = serializer.validated_data.pop('is_employer', False)
            if is_employer:
                User.objects.create_employer(**serializer.validated_data)
                message = '招聘者创建成功！'
            else:
                User.objects.create_user(**serializer.validated_data)
                message = '普通用户创建成功！'

            return APIResponse(code=200,msg=message,data=serializer.data)
        # {'error': '在创建用户时出现错误，请联系管理员'}

        return APIResponse(code=400,msg="用户名或密码错误",data=serializer.errors)


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

        # print(serializer)

        if serializer.is_valid():
            # print(serializer.data)
            serializer.save()
            return APIResponse(code=200,msg="个人信息更改成功",data=serializer.data)
        return APIResponse(code=400,msg="表单填写错误，请重新填写！",data=serializer.errors)


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