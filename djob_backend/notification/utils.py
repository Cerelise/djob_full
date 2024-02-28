from accounts.models import UserAccount
from company.models import Company
from jobs.models import CandidatesApplied, Job

from .models import Notification


def create_notification(request,type_of_notification,apply_id=None,company_id=None,job_id=None):
    created_for = None

    admin = UserAccount.objects.filter(is_superuser=True)[0]

    # content = None

    if type_of_notification == 'new_apply_request':
        apply_request = CandidatesApplied.objects.get(pk=apply_id)
        created_for = apply_request.created_for

        job_name = apply_request.job.title
        content = f'{request.user.name}提交了贵公司{job_name}的工作申请'

    elif type_of_notification == 'accept_apply_request':
        apply_request = CandidatesApplied.objects.get(pk=apply_id)
        created_for = apply_request.created_by

        if apply_request.status == '通过':
            content = f'恭喜您！您的求职申请已经通过！'
    
    elif type_of_notification == 'reject_apply_request':
        apply_request = CandidatesApplied.objects.get(pk=apply_id)
        created_for = apply_request.created_by

        if apply_request.status == '驳回':
            content = f'不好意思,您的求职未通过！'

    elif type_of_notification == 'new_job_request':
        
        job_request = Job.objects.filter(id=job_id).first()
        created_for = admin
        job_name = job_request.title
        content = f'{request.user.name}提供了{job_name}的详细信息，请尽快审核！'

    elif type_of_notification == 'accept_job_request':
        job_request = Job.objects.get(pk=job_id)
        created_for = job_request.employer
        if job_request.status == 1:
            content = f'您提交的 {job_request.title} 已被通过！'

    elif type_of_notification == 'reject_job_request':
        job_request = Job.objects.get(pk=job_id)
        created_for = job_request.employer

        if job_request.status == 0:
            content = f'您提交的 {job_request.title} 已被驳回。'

    elif type_of_notification == 'new_company_request':
        company_request = Company.objects.get(id=company_id)
        created_for = admin
        company_name = company_request.title
        content = f'{request.user.name}提供了{company_name}的详细信息，请尽快审核！'
    
    elif type_of_notification == 'accept_company_request':
        company_request = Company.objects.get(id=company_id)
        created_for = company_request.employer
        if company_request.status == 1:
            content = f'您提交的{company_request.title}公司信息已被通过！'

    elif type_of_notification == 'reject_company_request':
        company_request = Company.objects.get(id=company_id)
        created_for = company_request.employer
        if company_request.status == 0 and company_request.message:
            content = f'您提交的{company_request.title}公司信息未被通过！'


        
    notification = Notification.objects.create(
      content = content,
      created_by = request.user,
      type_of_notification=type_of_notification,
      created_for=created_for
    )

    return notification


        
