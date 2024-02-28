from accounts.serializers import UserSerializer,UserProfileSerializer
from company.serializers import CompanySerializer
from rest_framework import serializers

from .models import CandidatesApplied, Comment, Job, Reply


class ReplySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Reply
        fields = ('id','content','comment','created_by','created_at','type_of')

class CommitReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reply
        fields = ('id','content','comment','created_by')

class CommentSerializer(serializers.ModelSerializer):
    comment_replied = ReplySerializer(many=True,read_only=True)
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Comment
        fields = ('id','content','created_by','created_at','comment_replied','type_of')

class CommitCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content','created_by')


class JobSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True,many=True)
    company = CompanySerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    # employer = UserSerializer(read_only=True)
    class Meta:
        model = Job
        fields = "__all__"

class CommitJobSerializer(serializers.ModelSerializer):

      class Meta:
          model = Job
          fields = ('id','title','description','location','category','salary','vacancy','employer','company')

class UpdateJobSerializer(serializers.ModelSerializer):

      class Meta:
          model = Job
          fields = ('title','description','location','category','salary','vacancy')
        

class CandidatesAppliedSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_by = UserProfileSerializer()
    class Meta:
        model = CandidatesApplied
        fields = ('id','comment','status','resume','job','created_at','created_by')

