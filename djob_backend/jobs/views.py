from core.handler import APIResponse
from django.db.models import Avg, Count, Max, Min
from django.shortcuts import get_object_or_404
from notification.utils import create_notification
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import JobsFilter
from .models import CandidatesApplied, Job
from .permissions import (HandleAppicationIsEmployerOrReadOnly,
                          IsEmployerOrReadOnly)
from .serializers import (CandidatesAppliedSerializer, CommentSerializer,
                          JobSerializer, ReplySerializer)


def JobPaginator(page):
    paginator = PageNumberPagination()
    paginator.page_size = page
    return paginator

class JobListingAndCreateView(APIView):
    
    serializer_class = JobSerializer

    def get(self,request):

        filterset = JobsFilter(request.GET,queryset=Job.objects.filter(status=0))
        # print(filterset)
        # print(filterset.qs)
        # 岗位总量
        count = filterset.qs.count()
        # 分页设置
        resPerPage = 2 # 每页多少项
        paginator = PageNumberPagination()
        paginator.page_size = resPerPage

        queryset = paginator.paginate_queryset(filterset.qs,request)

        serializer = JobSerializer(queryset,many=True)

        new_data = []
        # counter = { 'job_count':count }
        # new_data.append(counter)
        for data in serializer.data:
            new_data.append(data)

        return Response({
          'message':"获取成功",
          'data':new_data,
        })
    
    def post(self,request):
        user = request.user

        if not user.is_employer and not user.is_superuser:
            return Response(
              {'message':'该用户没有足够的权限执行该操作，请联系管理员'},
              status=status.HTTP_403_FORBIDDEN
            )
        
        data = request.data
        employer = request.user.id
        data['employer'] = employer

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            
            new_job = serializer.save()
            # print(f'1:{new_job.id}')
            notification = create_notification(request,'new_job_request',job_id=new_job.id)

            response = {
              "message":"招聘信息提交成功！请等待管理员审核！",
              "data":serializer.data,
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)





class JobManagerView(APIView):
    permission_classes = [IsEmployerOrReadOnly]
    serilizer_class = JobSerializer

    def get(self,request,pk):
        job = get_object_or_404(Job,id=pk)
        job_serializer = self.serilizer_class(instance=job)

        return Response(
          {"detail":job_serializer.data},
          status=status.HTTP_200_OK
        )

    # def put(self,request,pk):
    #     job = get_object_or_404(Job,id=pk)
    #     self.check_object_permissions(request,job)
    #     data = request.data
    #     employer = request.user.id
    #     data['employer'] = employer

    #     serializer = self.serilizer_class(instance=job,data=data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         response = {
    #           "message":"招聘信息已更新！",
    #           "data":serializer.data
    #         }

    #         return Response(data=response,status=status.HTTP_200_OK)
    #     return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        job = get_object_or_404(Job,id=pk)
        self.check_object_permissions(request,job)

        job.delete()

        return Response({"message":"该招聘信息已删除！"},status=status.HTTP_200_OK)

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def applyToJob(request,pk):

    user = request.user
    job = get_object_or_404(Job,id=pk)

    if user.resume == '':
        return Response({'error':'请先上传简历！'},status=status.HTTP_400_BAD_REQUEST)
    
    alreadyApplied = CandidatesApplied.objects.filter(created_for=job.employer).filter(created_by=user)

    if alreadyApplied:
        return Response({'error':"您已经投过简历了"},status=status.HTTP_400_BAD_REQUEST)

    application = CandidatesApplied.objects.create(
        created_for=job.employer,
        created_by=user,
        resume=user.resume.name,
        job=job
    )

    notification = create_notification(request,'new_apply_request',apply_id=application.id)

    serializer = CandidatesAppliedSerializer(instance=application,many=False)
    response = {
        "message":"求职申请已提交！",
        "status":serializer.data['status']
    }

    return Response(data=response,status=status.HTTP_201_CREATED)
    # return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
  
class CandidatesAppliedListingViews(APIView):
    
    permission_classes = []
    serializer_class = CandidatesAppliedSerializer

    def get(self,request):

        listings = CandidatesApplied.objects.all()

        listings_serializer = self.serializer_class(listings,many=True)

        return Response({
          'listing':listings_serializer.data          
        },status=status.HTTP_200_OK)


class CandidatesAppliedManager(APIView):
    
    permission_classes = [HandleAppicationIsEmployerOrReadOnly]
    serializer_class = CandidatesAppliedSerializer 

    def get(self,request,pk):

        apply_detail = get_object_or_404(CandidatesApplied,id=pk)
        apply_serializer = self.serializer_class(instance=apply_detail)

        return Response(
          {"detail":apply_serializer.data},
          status=status.HTTP_200_OK
        )

    def put(self,request,pk):

        apply_detail = get_object_or_404(CandidatesApplied,id=pk)
        self.check_object_permissions(request,apply_detail)
        data = request.data
        update_detail = CandidatesApplied.objects.filter(id=pk).update(
            status=data['status'],
            comment=data['comment'],
        )

        apply_status = data['status']
        if apply_status == 'accepted':
            notification = create_notification(request,'accept_apply_request',apply_id=pk)

        elif apply_status == 'rejected':
            notification = create_notification(request,'reject_apply_request',apply_id=pk)

        detail = CandidatesApplied.objects.get(id=pk)

        apply_serializer = self.serializer_class(instance=detail)

        return Response(
          {
            "message":"求职申请已处理！",
            "detail":apply_serializer.data
          },
          status=status.HTTP_200_OK
        )

    def delete(self,request,pk):
        application = get_object_or_404(CandidatesApplied,id=pk)
        self.check_object_permissions(request,application)

        application.delete()

        return Response({"message":"已撤销该求职请求！"},status=status.HTTP_200_OK)


# comment of user
class CommentManagerView(APIView):

    permission_classes = []

    def post(self,request,pk):
        
        data = request.data

        comment_data = {
          "content":data['content'],
          "created_by":request.user.id
        }

        serializer = CommentSerializer(data=comment_data)

        if serializer.is_valid():

            comment = serializer.save()

            job = Job.objects.get(id=pk)
            job.comments_count = job.comments_count + 1
            job.comments.add(comment)

            job.save()

            response = {
              "message":"发布评论成功",
              "data":serializer.data
            }

            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ReplyManagerView(APIView):

    permission_classes = [IsEmployerOrReadOnly]

    serializer_class = ReplySerializer

    def post(self,request,pk):

        data = request.data

        reply_data = {
            "content":data['content'],
            "comment":pk,
            "created_by":request.user.id
        }

        serializer = self.serializer_class(data=reply_data)

        if serializer.is_valid():
            serializer.save()

            response = {
              "message":"回复发布成功",
              "data":serializer.data,
            }

            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        


