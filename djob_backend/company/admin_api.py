import os
import uuid

from django.shortcuts import get_object_or_404
from PIL import Image
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company
from .permissions import IsAdminUserOrReadOnly
from .serializers import CompanySerializer


class AdminCompanyListView(APIView):

    permission_classes = [IsAdminUserOrReadOnly]

    serializer_class = CompanySerializer

    def get(self,request):

        company_list = Company.objects.all()
        
        serializer = CompanySerializer(company_list,many=True)

        response = {
          "data":serializer.data
        }

        return Response(data=response,status=status.HTTP_200_OK)

    def post(self,request):

        data = request.data

        serializer = CompanySerializer(data=data)

        if serializer.is_vaild():

            serializer.save()

            response = {
              "message":"企业信息已录入！",
              "data":serializer.data
            }

            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AdminCompanyManagerView(APIView):

    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = CompanySerializer

    def get(self,request,pk):

        company = get_object_or_404(Companyid=pk)
        company_serializer = self.serializer_class(instance=company)

        response = {
          "data":company_serializer.data
        }

        return Response(
          data=response,
          status=status.HTTP_200_OK
        )

    def put(self,request,pk):
        company = get_object_or_404(company,id=pk)

        data = request.data

        serializer = self.serializer_class(instance=company,data=data)

        if serializer.is_valid():

            serializer.save()

            response = {
              "message":"该企业信息已更新!",
              "data":serializer.data
            }
            return Response(data=response,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,pk):
        company = get_object_or_404(company,id=pk)
        
        company.delete()

        response = {
          "message":"该企业信息已删除！"
        }

        return Response(data=response,status=status.HTTP_200_OK)
