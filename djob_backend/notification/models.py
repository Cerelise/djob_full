import uuid

from accounts.models import UserAccount
from company.models import Company
from django.db import models
from jobs.models import CandidatesApplied, Job


# 通知模型
class Notification(models.Model):
  # 通知类型声明
  NEWAPPLYREQUEST = 'new_apply_request'
  ACCEPTAPPLYREQUEST = 'accept_apply_request'
  REJECTAPPLYREQUEST = 'reject_apply_request'
  NEWJOBREQUEST = 'new_job_request'
  ACCEPTJOBREQUEST = 'accept_job_request'
  REJECTJOBREQUEST = 'reject_job_request'
  NEWCOMPANYREQUEST = 'new_company_request'
  ACCEPTCOMPANYREQUEST = 'accept_company_request'
  REJECTCOMPANYREQUEST = 'reject_company_request'

  # 初始化类型
  CHOICE_TYPE_OF_NOTIFICATION = {
      (NEWAPPLYREQUEST,'New applyrequest'),
      (ACCEPTAPPLYREQUEST,'Accept applyrequest'),
      (REJECTAPPLYREQUEST,'Reject applyrequest'),
      (NEWJOBREQUEST,'New jobrequest'),
      (ACCEPTJOBREQUEST,'Accept jobrequest'),
      (REJECTJOBREQUEST,'Reject jobreqeust'),
      (NEWCOMPANYREQUEST,'New companyrequest'),
      (ACCEPTCOMPANYREQUEST,'Accept companyrequest'),
      (REJECTCOMPANYREQUEST,'Reject companyreqeust'),
  }

  id = models.UUIDField(primary_key=True,default=uuid.uuid4)
  content = models.TextField()
  notification_status = models.SmallIntegerField(default=0) # 0 处理中 1 通过 2 未通过
  type_of_notification = models.CharField(max_length=50,choices=CHOICE_TYPE_OF_NOTIFICATION)
  application = models.ForeignKey(CandidatesApplied,on_delete=models.SET_NULL,blank=True,null=True)
  job = models.ForeignKey(Job,on_delete=models.SET_NULL,blank=True,null=True)
  company = models.ForeignKey(Company,on_delete=models.SET_NULL,blank=True,null=True)
  created_by = models.ForeignKey(UserAccount,related_name='created_notification',on_delete=models.SET_NULL,null=True)
  created_for = models.ForeignKey(UserAccount,related_name='received_notification',on_delete=models.SET_NULL,null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
     ordering = ['-created_at']
  
  def __str__(self) -> str:
    return f'{self.content}_{self.created_by}'

  
  

