from django.urls import path

from . import api, views

urlpatterns = [
  path('job-list',api.JobListingView.as_view()),
  path('job-detail/<uuid:pk>',api.JobManagerView.as_view()),
  path('apply-listing',api.CandidatesAppliedListingViews.as_view()),
  path('apply-detail/<uuid:pk>',api.CandidatesAppliedManager.as_view()),
  # 获取工作列表
  path('stats',api.getTopicStats,name='get_topic_stats'),
  path('<uuid:pk>/apply',api.applyToJob,name='apply_to_job'),
    # 获取类型
  path('category',api.getCategoriesKeyword,name="get_keywords"),
  # 评论/回复
  path('<uuid:pk>/comment-area',api.publishCommentOrReply,name="publish_comment"),
]

