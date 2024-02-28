from accounts.models import UserAccount
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
from .models import Job
from .permissions import IsAdminUserOrReadOnly
from .serializers import JobSerializer


# 管理员对所有工作的增删改查
class AdminJobListView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = JobSerializer

    def get(self,request):
        filterset = JobsFilter(request.GET,queryset=Job.objects.all())
        count = filterset.qs.count()

        serializer = JobSerializer(filterset.qs,many=True)

        res = {
          'message':'获取成功！',
          'job_count':count,
          'data':serializer.data
        }

        return Response(res,status=status.HTTP_200_OK)

    def post(self,request):
        
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():

            serializer.save()

            res = {
                "message":"新工作岗位已创建！",
                "data":serializer.data
            }

            return Response(res,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class AdminJobManagerView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = JobSerializer

    def get(self,requset,pk):
        job = get_object_or_404(Job,id=pk)
        job_serializer = self.serializer_class(instance=job)

        res = {
          "data":job_serializer.data
        }
        return Response(res,status=status.HTTP_200_OK)

    def put(self,request,pk):
        job = get_object_or_404(Job,id=pk)
        data = request.data
        
        serializer = self.serializer_class(instance=job,data=data)

        if serializer.is_valid():
            serializer.save()
            res = {
              "message":"该招聘信息已经更新！",
              "data":serializer.data
            }
            return Response(res,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk):
        job = get_object_or_404(Job,id=pk)

        job.delete()

        res = {
          "message":"该招聘信息已删除！"
        }

        return Response(data=res,status=status.HTTP_200_OK)
