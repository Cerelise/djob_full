import uuid

from accounts.models import UserAccount
from django.db import models
from django.utils import timezone


# Create your models here.
class Company(models.Model):
    employer = models.OneToOneField(UserAccount,related_name='company_emp',on_delete=models.CASCADE,null=True)
    avatar = models.CharField(null=True,max_length=500)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=255,null=True)
    description = models.TextField() # 公司简介
    address = models.CharField(max_length=500)
    company_type = models.CharField(max_length=100,null=True) # 行业
    staff_size = models.CharField(max_length=100,null=True) # 人数规模
    business_scope = models.TextField(null=True) # 经营范围
    captical = models.CharField(max_length=100,null=True)  # 注册资本
    job_count = models.IntegerField(default=0)  
 

    status = models.IntegerField(default=0)
    message = models.TextField(null=True,blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title

    

    

    

