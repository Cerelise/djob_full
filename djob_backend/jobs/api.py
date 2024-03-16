from accounts.models import UserAccount
from company.models import Company
from core.handler import APIResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from notification.models import Notification
from notification.utils import create_notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .filters import JobsFilter
from .models import CandidatesApplied, Comment, Job, Reply
from .permissions import (HandleAppicationIsEmployerOrReadOnly,
                          IsEmployerOrReadOnly)
from .serializers import (CandidatesAppliedSerializer, CommitCommentSerializer,
                          CommitJobSerializer, CommitReplySerializer,
                          JobSerializer, UpdateJobSerializer)


def JobPaginator(page):
    paginator = PageNumberPagination()
    paginator.page_size = page
    return paginator

# 工作管理类视图
class JobListingView(APIView):
    serializer_class = JobSerializer
    # 获取工作列表并分页
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
    # 创建工作信息
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
        serializer = CommitJobSerializer(data=data)
        if serializer.is_valid():         
            new_job = serializer.save()
            notification = create_notification(request,'new_job_request',job_id=new_job.id)
            current_job = Job.objects.filter(id=new_job.id).first()
            notification.job = current_job
            notification.save()
            return APIResponse(code=200,msg="招聘信息提交成功！请等待管理员审核！")
        return APIResponse(code=400,msg="表单填写错误，请重新填写后提交！",data=serializer.errors)

# 管理单个工作
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

# 工作申请函数
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
    notification.application = application
    notification.save()
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

# 管理工作申请(企业)类视图
class CandidatesAppliedManager(APIView):
    permission_classes = [HandleAppicationIsEmployerOrReadOnly]
    serializer_class = CandidatesAppliedSerializer 
    # 获取单个申请
    def get(self,request,pk):
        apply_detail = get_object_or_404(CandidatesApplied,id=pk)
        apply_serializer = self.serializer_class(instance=apply_detail)
        return APIResponse(code=200,msg="",data=apply_serializer.data)
    # 更新申请状态
    def put(self,request,pk):
        apply_detail = get_object_or_404(CandidatesApplied,id=pk)
        self.check_object_permissions(request,apply_detail)
        data = request.data
        update_detail = CandidatesApplied.objects.filter(id=pk).update(
            status=data['status']
        )
        apply_status = data['status']
        original_notice = Notification.objects.filter(application=apply_detail).first()
        if apply_status == '通过':
            notification = create_notification(request,'accept_apply_request',apply_id=pk)
            notification.notification_status = 1
            notification.save()
            original_notice.notification_status = 1
            original_notice.save()
        elif apply_status == '驳回':
            notification = create_notification(request,'reject_apply_request',apply_id=pk)
            notification.notification_status = 2
            notification.save()
            original_notice.notification_status = 2
            original_notice.save()
        detail = CandidatesApplied.objects.get(id=pk)
        detail.created_at = now()
        detail.save()
        apply_serializer = self.serializer_class(instance=detail)
        return APIResponse(code=200,msg="求职申请已处理！",data=apply_serializer.data)
    # 删除该申请
    def delete(self,request,pk):
        application = get_object_or_404(CandidatesApplied,id=pk)
        self.check_object_permissions(request,application)
        application.delete()
        return APIResponse(code=200,msg="已撤销该求职申请")

# 发布评论或回复的函数
@api_view(['POST'])
@permission_classes([])
def publishCommentOrReply(request,pk):
    user_id = request.user.id
    data = request.data
    content = data['content']
    user = UserAccount.objects.get(id=user_id)
    if data['comment_id'] == 'None':
        rate = data['rate']
        comment = Comment.objects.create(content=content, rate=rate,created_by=user)
        job = Job.objects.get(id=pk)
        job.comments_count = job.comments_count + 1
        job.comments.add(comment)
        comments_list = job.comments.all() 
        rate_list = []
        for comment in comments_list:
            rate_list.append(comment.rate)
        arr_sum = sum(rate_list)
        rate_mean = arr_sum / len(rate_list)
        job.average_rate = rate_mean
        job.save() 
    else:
        comment = Comment.objects.get(id=data['comment_id'])
        reply = Reply.objects.create(content=content,created_by=user,comment=comment)

    return APIResponse(code=200,msg="发布成功！")

    
# 条件查询函数，将结果分页并返回
@api_view(['GET'])
def getTopicStats(request):
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

# 获取所有在工作类别里的标签
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