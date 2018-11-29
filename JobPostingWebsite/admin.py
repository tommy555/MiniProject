from django.contrib import admin
from .models import Company, User, Jobs, JobApplication, Admin as ad, JobType, JobCategory, Skill

# Register your models here.

admin.site.register(Company)
admin.site.register(User)
admin.site.register(Jobs)
admin.site.register(JobApplication)
admin.site.register(ad)
admin.site.register(JobType)
admin.site.register(Skill)
admin.site.register(JobCategory)

