from django.urls import path

from . import api, verify_api, views

urlpatterns = [
    # 发送验证邮件
    path('verify',views.send_verify_email,name='verify_mail'),
    path('register', api.RegisterView.as_view()),
    path('login',api.LoginView.as_view()),
    path('me', api.UserProfileView.as_view()),
    path('resume',api.UpdateResumeView.as_view()),
    path('avatar',api.UploadAvatar,name="upload_avatar"),
    # 获取工作申请列表
    path('apply',verify_api.ApplyListForUserView.as_view()),
    path('apply-employer',verify_api.ApplyListForEmployerView.as_view()),
    # redis
    path('verify/set',views.store_verification_code,name="set_cache"),
    path('verify/get',views.get_verify_code,name="get_cache"),
]
