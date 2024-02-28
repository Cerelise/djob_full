from django.urls import path
from . import api

urlpatterns = [
  path('cp-list',api.CompanyListingView.as_view()),
  path('cp-detail/<uuid:pk>',api.CompanyManagerView.as_view()),
  path('cp/picture',api.uploadCompanyPhoto,name="upload_company_photo"),
  # 获取当前用户的企业信息
  path('detail',api.getCompanyDetails,name="get_company_details"),
]