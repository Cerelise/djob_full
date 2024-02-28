from django.contrib import admin

from .models import CandidatesApplied, Comment, Job, Reply

# Register your models here.
admin.site.register(Job)
admin.site.register(CandidatesApplied)
admin.site.register(Comment)
admin.site.register(Reply)
