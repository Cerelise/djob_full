from core.handler import APIResponse
from jobs.models import CandidatesApplied
from jobs.serializers import CandidatesAppliedSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView


class ApplyListForUserView(APIView):
      permission_classes = []

      def get(self,request):
          user_id = request.user.id
          user_apply = CandidatesApplied.objects.filter(created_by=user_id)
          
          
          pageinator = PageNumberPagination()
          pageinator.page_size = 5
          queryset = pageinator.paginate_queryset(user_apply,request)

          serializer = CandidatesAppliedSerializer(queryset,many=True)

          response = {
            'count':pageinator.page.paginator.count,
            'data':serializer.data
          }

          return APIResponse(code=200,msg="",data=response)

class ApplyListForEmployerView(APIView):
      permission_classes = []

      def get(self,request):
          user_id = request.user.id
          print(user_id)
          user_apply = CandidatesApplied.objects.filter(created_for=user_id)
          print(user_apply)

          pageinator = PageNumberPagination()
          pageinator.page_size = 5
          queryset = pageinator.paginate_queryset(user_apply,request)
          
          serializer = CandidatesAppliedSerializer(queryset,many=True)

          response = {
            'count':pageinator.page.paginator.count,
            'data':serializer.data
          }

          return APIResponse(code=200,msg="",data=response)
