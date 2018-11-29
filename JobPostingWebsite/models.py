"""
    data models
"""
from django.db import models

# Create your models here.

class JobCategory(models.Model):
    """ Job category data models """
    name = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    """ Company data models """
    email = models.CharField(max_length=250, null=True)
    username = models.CharField(max_length=250, null=True)
    company_reg = models.CharField(max_length=250, null=True)
    company_type = models.ForeignKey(JobCategory, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=250, null=True)
    town = models.CharField(max_length=250, null=True)
    state = models.CharField(max_length=250, null=True)
    country = models.CharField(max_length=250, null=True)
    password = models.CharField(max_length=250, null=True)
    spoken_lang = models.CharField(max_length=250, null=True)
    website = models.CharField(max_length=250, null=True)
    img = models.ImageField(upload_to="profile_image", blank=True, null=True)
    user_type = models.CharField(max_length=10, default="Company", null=True)
    desc = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.username

class User(models.Model):
    """ User data models """
    email = models.CharField(max_length=250, null=True)
    username = models.CharField(max_length=250, null=True)
    nric = models.CharField(max_length=12, null=True)
    skills = models.CharField(max_length=2500, null=True)
    contact = models.CharField(max_length=250, null=True)
    password = models.CharField(max_length=250, null=True)
    user_type = models.CharField(max_length=10, default="Normal", null=True)
    bio = models.CharField(max_length=2500, null=True)

    def __str__(self):
        return self.username

class Admin(models.Model):
    """ User data models """
    email = models.CharField(max_length=250, null=True)
    username = models.CharField(max_length=250, null=True)
    password = models.CharField(max_length=250, null=True)
    user_type = models.CharField(max_length=10, default="Admin", null=True)

    def __str__(self):
        return self.username

class JobType(models.Model):
    """ type of job data models """
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, null=True)

    def __str__(self):
        return "({}, {})".format(self.name, self.category.name)

class Jobs(models.Model):
    """ Jobs data models """
    name = models.CharField(max_length=250, null=True)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE, null=True)
    skill_required = models.CharField(max_length=2500, null=True)
    desc = models.CharField(max_length=2500, null=True)
    salary = models.FloatField(default=0, null=True)
    accessed_count = models.IntegerField(default=0, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    expired_date = models.DateField(null=True)
    is_approved = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return "({}, {})".format(self.name, self.company.username)

class JobApplication(models.Model):
    """ Job Application History """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)

    def __str__(self):
        return "({}, {})".format(self.user.username, self.job.name)

class Skill(models.Model):
    """ Skill List """
    name = models.CharField(max_length=250, null=True)
