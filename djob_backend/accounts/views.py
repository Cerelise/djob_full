import random

from core.handler import APIResponse
from django.core.mail import send_mail
from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import UserAccount


# 生成验证码
def generate_verification_code():
    code = ""
    for _ in range(6):
        digit = random.randint(0,9)
        code += str(digit)
    return code

@api_view(['POST'])
@permission_classes([AllowAny])
def send_verify_email(request):
    data = request.data
    email_address = data['email']

    verify_code = generate_verification_code()
    # 发送邮件
    send_mail(
              '完成您的账户注册',
              f'您的验证码为:{verify_code}，5分钟内有效，请尽快使用！',
              'cerelisezc@qq.com',
              [email_address],
              fail_silently=False,
    )
    # 设置redis
    redis_conn = get_redis_connection()
    res = redis_conn.set(email_address,verify_code)
    # 过期时间5min
    redis_conn.expire(email_address,500)

    return APIResponse(code=200,msg='验证码已经发送，请注意查收！')

def activateemail(request):
    email = request.GET.get('email','')
    id = request.GET.get('id','')

    if email and id:
        user = UserAccount.objects.get(id=id,email=email)
        user.is_active = True
        user.save()

        return HttpResponse('账号已激活!请您继续接下来的操作。')
    else:
        return HttpResponse('该账号似乎还未被创建，请重试！')

@api_view(['GET'])
def store_verification_code(request):
    code = generate_verification_code()
    redis_conn = get_redis_connection()
    id_str = str(request.user.id) 
    res = redis_conn.set(id_str,code)
    redis_conn.expire(id_str,500)

    return APIResponse(code=200,msg='验证码已经生成！')

@api_view(['GET'])
@permission_classes([AllowAny])
def get_verify_code(request):
    user_id = request.GET.get('id')
    redis_conn = get_redis_connection()
    stored_code = redis_conn.get(user_id)

    return APIResponse(code=200,msg="",data=stored_code)

