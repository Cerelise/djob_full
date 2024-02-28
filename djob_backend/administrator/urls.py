from django.urls import path

from .view import company, job, public, user

urlpatterns = [
  path('user/list',user.UserListView.as_view()),
  path('user/detail/<uuid:pk>',user.UserManagerView.as_view()),
  path('cj-list',public.FilterRecruitDataView.as_view()),
  path('verify/company/<uuid:pk>',company.VerifyCompany.as_view()),
  path('verify/job/<uuid:pk>',job.VerifyJob.as_view()),
  # 评论
  path('comment',job.AdminCommentReplyListView.as_view()),
  path('comment/detail',job.AdminCommentReplyManagerView.as_view()),
] 