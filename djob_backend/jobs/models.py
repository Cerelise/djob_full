import uuid

from accounts.models import UserAccount
from company.models import Company
from django.db import models
from django.utils import timezone


class Comment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    content = models.TextField(blank=True,null=True)
    rate = models.SmallIntegerField(default=0)
    created_by = models.ForeignKey(UserAccount,related_name='comments',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # 1是评论 2是回复
    type_of = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ['-created_at',]

    def __str__(self) -> str:
        return self.content

class Reply(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    content = models.TextField(blank=True,null=True)
    comment = models.ForeignKey(Comment,related_name='comment_replied',on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserAccount,related_name='replies',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    type_of = models.SmallIntegerField(default=2)

    class Meta:
        ordering = ['-created_at',]


class Job(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='job_company',blank=True,null=True)
    employer = models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='job_employer')
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=200)
    salary = models.IntegerField(default=0,blank=True)
    average_rate = models.FloatField(default=0) # 平均评分

    status = models.SmallIntegerField(default=0)
    message = models.TextField(blank=True,null=True)

    comments = models.ManyToManyField(Comment,related_name="job_comments",blank=True)
    comments_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

  
class CandidatesApplied(models.Model):
    # 设置请求状态
    PENDING = '处理中'
    ACCEPTED = '通过'
    REJECTED = '驳回'

    STATUS_CHOICES = (
      (PENDING,'Pending'),
      (ACCEPTED,'Accepted'),
      (REJECTED,'Rejected')
    )

    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name='applicants')
    created_by = models.ForeignKey(UserAccount,related_name='user_created_requests',on_delete=models.CASCADE)
    created_for = models.ForeignKey(UserAccount,related_name='employer_received_requests',on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    resume = models.CharField(max_length=200,null=True) 
    comment = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=PENDING)
    created_at = models.DateTimeField(default=timezone.now)     
       
    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.created_by.name}发送的{self.job.title}的申请'








