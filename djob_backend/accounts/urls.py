from django.urls import path

from . import api,verify_api

urlpatterns = [
    path('login',api.LoginView.as_view()),
    path('register', api.RegisterView.as_view()),
    path('me', api.UserProfileView.as_view()),
    path('resume',api.UpdateResumeView.as_view()),
    path('avatar',api.UploadAvatar,name="upload_avatar"),
    # 获取工作申请列表
    path('apply',verify_api.ApplyListForUserView.as_view()),
    path('apply-employer',verify_api.ApplyListForEmployerView.as_view()),
]
