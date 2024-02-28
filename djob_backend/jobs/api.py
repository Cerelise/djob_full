from company.models import Company
from core.handler import APIResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from notification.utils import create_notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from accounts.models import UserAccount

from .filters import JobsFilter
from .models import CandidatesApplied, Job,Comment,Reply
from .permissions import (HandleAppicationIsEmployerOrReadOnly,
                          IsEmployerOrReadOnly)
from .serializers import (CandidatesAppliedSerializer, CommentSerializer,CommitCommentSerializer,
                          CommitJobSerializer, JobSerializer, ReplySerializer,CommitReplySerializer,
                          UpdateJobSerializer)


def JobPaginator(page):
    paginator = PageNumberPagination()
    paginator.page_size = page
    return paginator

class JobListingView(APIView):

    serializer_class = JobSerializer

    def get(self,request):

        filterset = JobsFilter(request.GET,queryset=Job.objects.filter(status=1))

        # 岗位总量
        count = filterset.qs.count()
        # 分页设置
        pageinator = JobPaginator(page=5)
        queryset = pageinator.paginate_queryset(filterset.qs,request)

        serializer = JobSerializer(queryset,many=True)

        response = {
          'count':count,
          'data':serializer.data
        }

        return APIResponse(code=200,msg="",data=response)

    def post(self,request):
        user = request.user

        if not user.is_employer and not user.is_superuser:
            return APIResponse(
              code=400,
              msg="该用户没有足够的权限执行该操作，请联系管理员"
            )
        
        data = request.data
        employer_id = request.user.id
        data['employer'] = employer_id

        company = Company.objects.get(employer=user.id)
        company_id = company.id
        data['company'] = company_id

        # print(data)

        serializer = CommitJobSerializer(data=data)
        if serializer.is_valid():
            
            new_job = serializer.save()
            # print(f'1:{new_job.id}')
            notification = create_notification(request,'new_job_request',job_id=new_job.id)

            return APIResponse(code=200,msg="招聘信息提交成功！请等待管理员审核！")
        return APIResponse(code=400,msg="表单填写错误，请重新填写后提交！",data=serializer.errors)

class JobManagerView(APIView):
    permission_classes = [IsEmployerOrReadOnly]
    serializer_class = JobSerializer

    def get(self,request,pk):
        job = get_object_or_404(Job,id=pk)
        job_serializer = self.serializer_class(instance=job)

        return APIResponse(code=200,msg="",data=job_serializer.data)

    def put(self,request,pk):
        job = get_object_or_404(Job,id=pk)
        self.check_object_permissions(request,job)
        
        data = request.data

        serializer = UpdateJobSerializer(instance=job,data=data)

        if serializer.is_valid():
            job = serializer.save()
            updated_job = Job.objects.filter(id=job.id).update(
              status=0,message=""
            )
            notification = create_notification(request,'new_job_request',job_id=job.id)

            return APIResponse(code=200,msg="招聘信息更新已提交，请等待管理员审核！")
        return APIResponse(code=400,msg="信息填写错误，请重新填写！")

    
    def delete(self,request,pk):
        job = get_object_or_404(Job,id=pk)

        self.check_object_permissions(request,job)

        job.delete()

        return APIResponse(code=200,msg="该招聘信息已删除！")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def applyToJob(request,pk):

    user = request.user
    job = get_object_or_404(Job,id=pk)

    if user.resume == '':
        return APIResponse(code=400,msg="请先上传简历！")
    
    alreadyApplied = CandidatesApplied.objects.filter(created_for=job.employer).filter(created_by=user)

    if alreadyApplied:
        return APIResponse(code=400,msg="您已经投过简历了")

    application = CandidatesApplied.objects.create(
        created_for=job.employer,
        created_by=user,
        resume=user.resume.name,
        job=job
    )

    notification = create_notification(request,'new_apply_request',apply_id=application.id)

    serializer = CandidatesAppliedSerializer(instance=application,many=False)
    response = {
        "status":serializer.data['status']
    }

    return APIResponse(code=200,msg="求职申请已提交",data=response)


class CandidatesAppliedListingViews(APIView):
    
    permission_classes = []
    serializer_class = CandidatesAppliedSerializer

    def get(self,request):

        listings = CandidatesApplied.objects.all()

        listings_serializer = self.serializer_class(listings,many=True)

        return APIResponse(code=200,msg=",",data=listings_serializer.data)

class CandidatesAppliedManager(APIView):
    
    permission_classes = [HandleAppicationIsEmployerOrReadOnly]
    serializer_class = CandidatesAppliedSerializer 

    def get(self,request,pk):

        apply_detail = get_object_or_404(CandidatesApplied,id=pk)
        apply_serializer = self.serializer_class(instance=apply_detail)

        return APIResponse(code=200,msg="",data=apply_serializer.data)

    def put(self,request,pk):

        apply_detail = get_object_or_404(CandidatesApplied,id=pk)
        self.check_object_permissions(request,apply_detail)
        data = request.data
        update_detail = CandidatesApplied.objects.filter(id=pk).update(
            status=data['status']
        )

        apply_status = data['status']
        if apply_status == '通过':
            notification = create_notification(request,'accept_apply_request',apply_id=pk)
            notification.notification_status = 1
            notification.save()

        elif apply_status == 'rejected':
            notification = create_notification(request,'reject_apply_request',apply_id=pk)
            notification.notification_status = 2
            notification.save()

        detail = CandidatesApplied.objects.get(id=pk)
        detail.created_at = now()
        detail.save()

        apply_serializer = self.serializer_class(instance=detail)

        return APIResponse(code=200,msg="求职申请已处理！",data=apply_serializer.data)

    def delete(self,request,pk):
        application = get_object_or_404(CandidatesApplied,id=pk)
        self.check_object_permissions(request,application)

        application.delete()

        return APIResponse(code=200,msg="已撤销该求职申请")

class CommentManagerView(APIView):

    permission_classes = []

    def post(self,request,pk):
        
        data = request.data

        comment_data = {
          "content":data['content'],
          "created_by":request.user.id
        }

        serializer = CommitCommentSerializer(data=comment_data)

        if serializer.is_valid():

            comment = serializer.save()

            job = Job.objects.get(id=pk)
            job.comments_count = job.comments_count + 1
            job.comments.add(comment)

            job.save()

            return APIResponse(code=200,msg="发布评论成功",data=serializer.data)
        return APIResponse(code=200,msg="发布评论失败，请重新提交",data=serializer.errors)


class ReplyManagerView(APIView):

    permission_classes = [IsEmployerOrReadOnly]

    serializer_class = CommitReplySerializer

    def post(self,request):

        data = request.data

        reply_data = {
            "content":data['content'],
            "comment":data['comment'],
            "created_by":request.user.id
        }

        serializer = self.serializer_class(data=reply_data)

        if serializer.is_valid():
            serializer.save()

            return APIResponse(code=200,msg="评论回复已发布",data=serializer.data)
        return APIResponse(code=400,msg="评论回复发送失败，请重试",data=serializer.errors)

@api_view(['POST'])
@permission_classes([])
def publishCommentOrReply(request,pk):
    user_id = request.user.id

    data = request.data
    content = data['content']
    user = UserAccount.objects.get(id=user_id)

    if data['comment_id'] == 'None':
        comment = Comment.objects.create(content=content, created_by=user)
        job = Job.objects.get(id=pk)
        job.comments_count = job.comments_count + 1
        job.comments.add(comment)

        job.save() 
    else:
        comment = Comment.objects.get(id=data['comment_id'])
        reply = Reply.objects.create(content=content,created_by=user,comment=comment)

        

    return APIResponse(code=200,msg="发布成功！")

    

@api_view(['GET'])
def getTopicStats(request):

    # args = { 'keyword__icontains':topic }
    job_list = Job.objects.filter(status=1)
    filter = JobsFilter(request.GET,queryset=job_list)

    if filter.is_valid():
        filterset = filter.qs
    else:
        filterset = Job.objects.filter(status=1,many=True)

    count = filter.qs.count()
    pageinator = JobPaginator(page=5)
    queryset = pageinator.paginate_queryset(filterset,request)

    serializer = JobSerializer(queryset,many=True)

    response = {
        'count':count,
        'data':serializer.data
    }

    return APIResponse(code=200,msg="",data=response)

@api_view(['GET'])
def getCategoriesKeyword(request):

    job_list = Job.objects.filter(status=1)

    categories = job_list.values_list('category',flat=True)

    category_keyword = ""
    for keyword in categories:
        category_keyword += f",{keyword}"
    
    category_list = category_keyword.split(',')
    word_list = list(set(category_list))
    filtered_category = ",".join(word_list).strip(',')


    return APIResponse(code=200,msg="",data=filtered_category)