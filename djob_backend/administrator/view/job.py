from core.handler import APIResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from jobs.models import Comment, Job, Reply
from jobs.permissions import IsEmployerOrReadOnly
from jobs.serializers import CommentSerializer, JobSerializer, ReplySerializer
from notification.models import Notification
from notification.utils import create_notification
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView


def AccountPaginator(page):
    paginator = PageNumberPagination()
    paginator.page_size = page
    return paginator

class VerifyJob(APIView):
    permission_classes = [IsEmployerOrReadOnly]
    def post(self,request,pk):

        data = request.data
        # 0为不通过 1为通过
        job_status = data['status']

        verified_job = Job.objects.filter(id=pk).update(
          status=job_status,
        )
        original_notice = Notification.objects.filter(job=pk).first()
        if job_status == 1:
            notification = create_notification(request,'accept_job_request',job_id=pk)
            notification.notification_status = 1
            notification.save()
            original_notice.notification_status = 1
            original_notice.save()
        elif job_status == 2 :
            notification = create_notification(request,'reject_job_request',job_id=pk)
            notification.notification_status = 2
            notification.save()
            original_notice.notification_status = 2
            original_notice.save()

        job_detail = Job.objects.get(id=pk)
        job_detail.created_at = now()
        job_detail.save()

        job_serializer = JobSerializer(job_detail)

        return APIResponse(
          code=200,
          msg='兼职信息申请已处理！',
          data=job_serializer.data
        )

class AdminCommentReplyListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        listing_comment = Comment.objects.all()
        listing_reply = Reply.objects.all()

        comment_serializer = CommentSerializer(listing_comment,many=True)
        reply_serializer = ReplySerializer(listing_reply,many=True)

        comment_data = comment_serializer.data
        reply_data = reply_serializer.data

        merged_data = comment_data + reply_data

        return APIResponse(code=200,msg='',data=merged_data)

class AdminCommentReplyManagerView(APIView):
      permission_classes = [IsAdminUser]


      def delete(self,request):
        
          data = request.data

          detail_id = data['id']
          type_of = data['type']

          print(type_of)
          if type_of == '1':
              detail = get_object_or_404(Comment,id=detail_id)
              detail.delete()

              return APIResponse(code=200,msg='评论删除完成')
          elif type_of == '2':
              detail = get_object_or_404(Reply,id=detail_id)
              detail.delete()

              return APIResponse(code=200,msg='回复删除完成')
          
          return APIResponse(code=400,msg='发生错误，请检查')










   
    



